import re
from urllib.parse import urlparse
from src.utils import clamp, has_any, extract_urls, extract_domains

def analyze_message(content: str, input_type: str):
    text = content.strip()
    lower = text.lower()
    urls = extract_urls(text)
    domains = extract_domains(urls)

    official_words = ["銀行","郵局","宅配","物流","海關","警察","檢察官","法院","政府","客服","官方","平台","金管會","稅務","電信","健保","蝦皮","momo","pchome","line官方","paypal","amazon"]
    urgency_words = ["立即","馬上","限時","最後通知","逾期","停用","凍結","鎖定","否則","24小時","驗證","立刻","今天內","即將失效","緊急"]
    threat_words = ["帳戶將被凍結","停權","停用","鎖定","取消資格","法律責任","違規","異常登入","帳戶異常","交易異常","安全風險"]
    money_words = ["匯款","轉帳","投資","獲利","保證收益","中獎","退款","帳戶","手續費","保證金","儲值","虛擬貨幣","加密貨幣","報酬","收益"]
    sensitive_words = ["密碼","驗證碼","otp","OTP","身分證","信用卡","卡號","cvv","個資","銀行帳號","帳號","登入","重新驗證","身份驗證"]
    secrecy_words = ["不要告訴","保密","私下","不要報警","只能你知道","私訊","加line","加入群組","老師帶單","內線","限量名額"]
    short_url_words = ["bit.ly","tinyurl","reurl","goo.gl","t.co","shorturl","is.gd","cutt.ly"]
    suspicious_domain_words = ["login","verify","secure","account","update","support","bank","wallet","bonus","claim","free","gift","service"]

    has_official = has_any(text, official_words)
    has_urgency = has_any(text, urgency_words)
    has_threat = has_any(text, threat_words)
    has_money = has_any(text, money_words)
    has_sensitive = has_any(text, sensitive_words)
    has_secrecy = has_any(text, secrecy_words)
    has_short_url = has_any(lower, short_url_words)
    has_url = len(urls) > 0
    has_suspicious_domain = any(any(k in d for k in suspicious_domain_words) for d in domains)
    has_ip_url = any(re.search(r"https?://\d{1,3}(\.\d{1,3}){3}", u) for u in urls)

    evidence = []
    if has_official: evidence.append("訊息提到官方、銀行、郵局、宅配、客服或政府機關等可信任名義。")
    if has_urgency: evidence.append("訊息使用立即、限時、凍結、停用或驗證等緊急壓迫語氣。")
    if has_threat: evidence.append("訊息帶有帳戶異常、停權、法律責任或安全風險等威脅語句。")
    if has_money: evidence.append("訊息涉及匯款、轉帳、投資、退款、中獎或收益誘導。")
    if has_sensitive: evidence.append("訊息要求或暗示輸入密碼、驗證碼、信用卡、身分證或帳號資料。")
    if has_secrecy: evidence.append("訊息要求私下處理、保密、加入群組或避免向外查證。")
    if has_url: evidence.append("訊息包含外部連結，可能導向釣魚網站。")
    if has_short_url: evidence.append("訊息包含短網址，容易隱藏真實目的地。")
    if has_suspicious_domain: evidence.append("連結網域包含 login、verify、secure、account、update 等常見釣魚字樣。")
    if has_ip_url: evidence.append("連結直接使用 IP 位址，通常不是正式服務的正常做法。")

    source_score = clamp(1.5 + (1 if input_type.lower() in ["sms","email","簡訊"] else 0) + (3 if has_official else 0) + (1.5 if has_url and has_official else 0) + (1.5 if has_secrecy else 0))
    semantic_score = clamp(1 + (3.2 if has_urgency else 0) + (2 if has_threat else 0) + (1.8 if has_money else 0) + (1.5 if has_secrecy else 0))
    link_score = clamp(0.8 + (3.3 if has_url else 0) + (2.4 if has_short_url else 0) + (1.5 if has_suspicious_domain else 0) + (2 if has_sensitive else 0) + (2 if has_ip_url else 0))
    context_score = clamp(1.2 + (3 if has_official and has_url else 0) + (2.2 if has_official and has_sensitive else 0) + (1.8 if has_money and has_urgency else 0) + (1.8 if has_threat and has_sensitive else 0) + (1.4 if has_secrecy and has_money else 0))

    weighted_score = round(source_score*0.23 + semantic_score*0.27 + link_score*0.28 + context_score*0.22, 1)

    critical_reasons = []
    if has_official and has_url and (has_sensitive or has_urgency):
        weighted_score = max(weighted_score, 8.2)
        critical_reasons.append("自稱官方或可信任單位，並要求透過連結驗證或立即處理。")
    if has_short_url and (has_urgency or has_sensitive):
        weighted_score = max(weighted_score, 8.0)
        critical_reasons.append("短網址搭配緊急或敏感資料要求，屬於典型釣魚組合。")
    if has_sensitive and has_url:
        weighted_score = max(weighted_score, 7.8)
        critical_reasons.append("同時出現外部連結與帳密、驗證碼或個資要求。")
    if has_money and has_urgency and (has_secrecy or has_url):
        weighted_score = max(weighted_score, 7.6)
        critical_reasons.append("金錢誘導搭配緊急壓迫與私下處理，社交工程風險高。")

    has_any_risk_signal = any([has_official, has_urgency, has_threat, has_money, has_sensitive, has_secrecy, has_url, has_short_url, has_suspicious_domain, has_ip_url])

    if weighted_score >= 7:
        classification = "RED"
        risk_label = "紅色魚：高風險詐騙"
        fish = "🔴🐟"
        short_title = "高風險，請勿操作"
        advice = ["不要點擊訊息中的任何連結。","不要輸入帳號、密碼、驗證碼、信用卡或身分證資料。","請改用官方 App、官方網站或官方客服電話查證。","如果已經輸入資料，請立即更改密碼並聯絡銀行或相關平台。","可將訊息截圖保存，必要時向 165 反詐騙專線或學校／公司資安窗口詢問。"]
    elif weighted_score >= 4 or has_any_risk_signal:
        classification = "YELLOW"
        risk_label = "黃色魚：中風險可疑訊息"
        fish = "🟡🐟"
        short_title = "可疑，建議先查證"
        advice = ["先不要急著回覆或點擊連結。","確認寄件者、電話號碼、Email 或 LINE 帳號是否真實。","若涉及金錢、帳號或個資，請直接向官方查證。","不要只依照訊息內提供的連結或電話聯絡。"]
    else:
        classification = "GREEN"
        risk_label = "綠色魚：低風險訊息"
        fish = "🟢🐟"
        short_title = "目前未見明顯詐騙特徵"
        advice = ["目前未偵測到明顯詐騙特徵。","仍建議不要隨意提供個人資料。","若訊息來源不明，仍可進一步查證。"]

    scam_types = []
    if has_official: scam_types.append("冒名官方／冒名客服")
    if has_urgency or has_threat: scam_types.append("緊急壓迫型社交工程")
    if has_url: scam_types.append("釣魚連結")
    if has_short_url: scam_types.append("短網址偽裝")
    if has_money: scam_types.append("金錢／投資／匯款誘導")
    if has_sensitive: scam_types.append("個資或驗證碼竊取")
    if has_secrecy: scam_types.append("私下處理／隔離查證")
    if not scam_types: scam_types.append("未偵測到明顯詐騙類型")

    if not evidence:
        evidence.append("目前沒有偵測到明顯的緊急壓迫、釣魚連結、金錢誘導或敏感資料要求。")
    if critical_reasons:
        evidence = critical_reasons + evidence

    agents = [
        {"name":"訊息來源辨識代理","score":round(source_score,1),"finding":"檢查是否冒名官方、客服、銀行、郵局、宅配或其他可信任單位。","reasoning":"若訊息以可信任名義出現，卻要求使用者立即點擊外部連結或私下處理，來源可信度會下降。"},
        {"name":"社交工程語意分析代理","score":round(semantic_score,1),"finding":"檢查是否使用恐嚇、急迫、利誘或情緒操控語句。","reasoning":"詐騙常透過凍結、逾期、限時、中獎、保證收益等語句，讓使用者在壓力下快速行動。"},
        {"name":"連結與敏感資訊檢查代理","score":round(link_score,1),"finding":"檢查短網址、陌生連結、可疑網域與敏感資料要求。","reasoning":"若同時出現連結與密碼、驗證碼、信用卡、身分證等要求，會被視為高風險釣魚特徵。"},
        {"name":"冒名與情境一致性代理","score":round(context_score,1),"finding":"檢查訊息主張與要求是否符合正常情境。","reasoning":"例如官方通知通常不會要求透過陌生短網址輸入驗證碼，也不會要求私下匯款或保密處理。"}
    ]

    return {
        "classification": classification,
        "risk_label": risk_label,
        "risk_score": weighted_score,
        "fish": fish,
        "short_title": short_title,
        "summary": f"多代理系統綜合訊息來源、語意操控、連結與情境一致性後，判定總風險分數為 {weighted_score}/10，因此釣出：{risk_label}。",
        "scam_types": scam_types,
        "evidence": evidence,
        "agents": agents,
        "advice": advice
    }
