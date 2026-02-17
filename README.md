# UK Weather Dashboard

Automated weather data pipeline that collects 3-day forecasts for 15 UK cities, with data visualization in Power BI.

## 📋 Project Overview

This project automatically collects weather forecast data every three days using the WeatherAPI.com API, stores the data in Excel, and provides interactive dashboards for analysis and visualization.

## 🎯 Features

- Automated data collection for 15 UK cities
- 3-day weather forecasts including temperature, conditions, and sunrise/sunset times
- Scheduled execution using Windows Task Scheduler (Every 3 days)
- Data storage in Excel format for easy access
- Power BI dashboard for data visualization

## 🛠️ Technologies Used

- **Python** - Data collection and processing
- **WeatherAPI.com** - Weather data source
- **Pandas** - Data manipulation
- **Windows Task Scheduler** - Automation
- **Power BI** - Dashboard and visualization
- **Excel** - Data storage
- **CLaude AI** - AI Chatbot

## 📂 Project Structure
```
UK_Weather_Dashboard/
├── scripts/           # Python data collection scripts
├── data/
│   ├── raw/          # Raw API responses
├── dashboards/       # Power BI files
```

## 🚀 Getting Started

### Running the Script
```bash
python scripts/your_script_name.py
```

## 📊 Data Sources

- [WeatherAPI.com](https://www.weatherapi.com/) - Free tier API for weather forecasts

## 🔮 Future Enhancements

- Weather alerts and notifications
- Additional UK cities
- Automated reporting via email

## 👤 Author

**Alfie Yearsley**  
Data Analyst | Leonard Curtis  


*This project is part of my data analytics portfolio showcasing automated data pipelines and business intelligence solutions.*
