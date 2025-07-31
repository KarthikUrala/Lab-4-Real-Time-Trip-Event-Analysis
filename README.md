# Lab-4-Real-Time-Trip-Event-Analysis

## 📌 Overview
This project is part of **CST8917 Lab 4** and implements a **real-time taxi trip monitoring system** using **Azure Event Hub**, **Azure Function**, **Azure Logic Apps**, and **Microsoft Teams**.  

The solution:
- Ingests real-time taxi trip data via Event Hub  
- Analyzes incoming trips for unusual patterns  
- Sends rich **Adaptive Card alerts** to Microsoft Teams  
- Helps supervisors detect fraud, suspicious vendor activity, or group rides instantly  

---

## 🏗️ Architecture

### **Components**
- **Azure Event Hub:** Captures simulated taxi trip events (`vendorID`, `tripDistance`, `passengerCount`, `paymentType`).
- **Azure Function:** Decodes Base64 events, analyzes for anomalies (`LongTrip`, `GroupRide`, `CashPayment`, `SuspiciousVendorActivity`).
- **Azure Logic App:** 
  - Triggered by Event Hub messages  
  - Sends data to Azure Function  
  - Loops through analyzed trips  
  - Posts Adaptive Cards to Microsoft Teams
- **Microsoft Teams:** Receives alerts for interesting or normal trips.

### **Architecture Diagram**
<img width="711" height="710" alt="Image" src="https://github.com/user-attachments/assets/4535b517-92b7-413a-8992-1cec0ae75135" />

---

## ⚙️ Setup Steps

### 1️⃣ Event Hub
- Created namespace and Event Hub `trip-events`.
- Configured Shared Access Policies with Manage rights.
- Python script `send-events.py` sends simulated JSON trip events.

### 2️⃣ Azure Function
- Function `analyze_trip` processes events:
  - Decodes Base64
  - Flags anomalies
  - Returns JSON summary.

### 3️⃣ Logic App
- Trigger: Event Hub (batch mode).
- HTTP action: Sends events to Azure Function.
- For Each loop: Iterates analyzed trips.
- Conditional routing:
  - 🚨 **Interesting trips** → Adaptive Card.
  - ✅ **Normal trips** → No-issue card.
  - ⚠️ **Suspicious vendor activity** → Special alert.

### 4️⃣ Microsoft Teams
- Logic App posts Adaptive Cards to Teams channel `nothing` for real-time monitoring.

---

## 🔑 Azure Function Logic

### Detection Rules
- **Long Trip:** Distance > 10 miles  
- **Group Ride:** Passenger count > 4  
- **Cash Payment:** PaymentType = 2  
- **Suspicious Vendor Activity:** Cash payment and distance < 1

### Logic App Workflow

- Trigger: Event Hub (batch mode)
- HTTP Action: Sends events to Azure Function
- For Each: Iterates analyzed trips
- Condition: Checks isInteresting
- Teams Posting: Adaptive cards sent accordingly

### Lessons Learned

- Handling Base64 decoding for Event Hub messages is crucial
- Configuring consumer groups ensures no event loss
- Adaptive Cards improve visibility in Teams
- Real-time event-driven architecture reduces manual monitoring

# Youtube Video- 

### Sample Output
```json
[
  {
    "vendorID": "V1",
    "tripDistance": 12.3,
    "passengerCount": 6,
    "paymentType": "2",
    "insights": ["LongTrip", "GroupRide", "CashPayment"],
    "isInteresting": true,
    "summary": "3 flags: LongTrip, GroupRide, CashPayment"
  }
]



