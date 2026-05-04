#!/bin/bash
# ============================================================
# AddyLabs Weekly Report
# Runs every Monday at 8am — emails summary to Gmail
# ============================================================

DATE=$(date '+%Y-%m-%d')
REPORT_FILE="/home/ubuntu/addylabs/outputs/weekly_report_${DATE}.txt"
ONPREM_REPORTS="lawborn@10.0.0.1:/home/lawborn/shared/reports/"

echo "=== AddyLabs Weekly Infrastructure Report ===" > $REPORT_FILE
echo "Generated: $(date)" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Run monitor agent
echo "--- INFRASTRUCTURE STATUS ---" >> $REPORT_FILE
python3 /home/ubuntu/addylabs/agents/monitor_agent.py >> $REPORT_FILE 2>&1

echo "" >> $REPORT_FILE

# Run weather agent
echo "--- WEEKLY WEATHER OUTLOOK ---" >> $REPORT_FILE
python3 /home/ubuntu/addylabs/agents/weather_agent.py >> $REPORT_FILE 2>&1

echo "" >> $REPORT_FILE

# Disk and service summary
echo "--- QUICK STATS ---" >> $REPORT_FILE
echo "Disk usage: $(df -h / | tail -1 | awk '{print $5}')" >> $REPORT_FILE
echo "Memory: $(free -h | grep Mem | awk '{print $3"/"$2}')" >> $REPORT_FILE
echo "Uptime: $(uptime -p)" >> $REPORT_FILE
echo "LiteLLM models: $(curl -s http://localhost:4000/models | python3 -m json.tool | grep '"id"' | wc -l) active" >> $REPORT_FILE

# Email the report
mail -s "AddyLabs Weekly Report - ${DATE}" lbornacelli@gmail.com < $REPORT_FILE

# Deliver to shared folder
scp $REPORT_FILE $ONPREM_REPORTS

echo "Weekly report sent and delivered!"
