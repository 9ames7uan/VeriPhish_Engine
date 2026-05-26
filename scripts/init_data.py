import os
import pandas as pd

training_data = [
    # 高風險 RED
    {
        "message": "【銀行通知】您的帳戶發生異常登入，請立即點擊 https://bit.ly/bank-verify 重新驗證帳號密碼與OTP驗證碼，否則24小時內將凍結帳戶。",
        "input_type": "SMS",
        "label": "RED",
        "scam_type": "假銀行釣魚"
    },
    {
        "message": "您的包裹配送失敗，請立即點擊 http://reurl.cc/fake 更新收件地址與信用卡資料，否則包裹將退回。",
        "input_type": "SMS",
        "label": "RED",
        "scam_type": "假包裹釣魚"
    },
    {
        "message": "我是公司主管，現在有一筆緊急款項需要你先轉帳處理，請不要告訴其他人，完成後私訊我。",
        "input_type": "LINE",
        "label": "RED",
        "scam_type": "假主管匯款"
    },
    {
        "message": "恭喜您中獎，請立即填寫身分證、銀行帳號與驗證碼領取獎金。",
        "input_type": "Email",
        "label": "RED",
        "scam_type": "假中獎個資詐騙"
    },
    {
        "message": "加入投資群組，老師帶你穩定獲利，每週保證收益30%，名額有限請立即加入LINE。",
        "input_type": "Chat",
        "label": "RED",
        "scam_type": "假投資群組"
    },

    # 中風險 YELLOW
    {
        "message": "您的包裹配送狀態異常，請盡快確認收件資訊。",
        "input_type": "SMS",
        "label": "YELLOW",
        "scam_type": "疑似包裹通知"
    },
    {
        "message": "您的帳戶有一筆異常登入紀錄，若非本人操作請盡快確認。",
        "input_type": "Email",
        "label": "YELLOW",
        "scam_type": "疑似帳戶異常通知"
    },
    {
        "message": "客服通知您目前有一筆退款待確認，請回覆是否需要協助。",
        "input_type": "LINE",
        "label": "YELLOW",
        "scam_type": "疑似假客服"
    },
    {
        "message": "系統偵測到您的資料可能尚未完成更新，請稍後進行確認。",
        "input_type": "Email",
        "label": "YELLOW",
        "scam_type": "疑似資料更新通知"
    },
    {
        "message": "您的會員資格即將到期，請留意後續通知。",
        "input_type": "SMS",
        "label": "YELLOW",
        "scam_type": "疑似會員通知"
    },

    # 低風險 GREEN
    {
        "message": "明天下午三點開會，請記得帶筆電與報告資料。",
        "input_type": "LINE",
        "label": "GREEN",
        "scam_type": "正常通知"
    },
    {
        "message": "老師提醒大家下週一要繳交期末報告。",
        "input_type": "LINE",
        "label": "GREEN",
        "scam_type": "正常學校通知"
    },
    {
        "message": "今晚一起吃飯嗎？我大概六點到。",
        "input_type": "Chat",
        "label": "GREEN",
        "scam_type": "正常聊天"
    },
    {
        "message": "會議記錄已整理完成，請大家有空時查看附件。",
        "input_type": "Email",
        "label": "GREEN",
        "scam_type": "正常工作信件"
    },
    {
        "message": "您的訂單已送達，感謝您的購買。",
        "input_type": "SMS",
        "label": "GREEN",
        "scam_type": "正常通知"
    },
]

df = pd.DataFrame(training_data)
df.to_csv("data/phishing_training_data.csv", index=False, encoding="utf-8-sig")
print("✅ Created data/phishing_training_data.csv")
