import requests
import pandas as pd
from datetime import datetime
import os
import time

API_KEY = 'Insert-Your-API-KEY-Here'
BASE_URL = 'http://api.weatherapi.com/v1/forecast.json'

CITIES = [
    'Manchester', 'London', 'Birmingham', 'Liverpool', 'Leeds',
    'Newcastle', 'Sheffield', 'Bristol', 'Edinburgh', 'Glasgow',
    'Cardiff', 'Belfast', 'Rochdale', 'Brighton', 'Oxford'
]

OUTPUT_DIR = r'C:\Users\Alfie.Yearsley\Downloads\Python\Weather Project'
SNAPSHOTS_DIR = os.path.join(OUTPUT_DIR, 'snapshots')
FORECAST_DAYS = 3

def get_weather_data(city):
    params = {
        'key': API_KEY,
        'q': f'{city},UK',
        'days': FORECAST_DAYS,
        'aqi': 'no',
        'alerts': 'no'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {city}: {e}")
        return None

def process_weather_data(weather_json, city):
    if not weather_json:
        return None
    
    snapshot_time = datetime.now()
    records = []
    
    try:
        location = weather_json['location']
        current = weather_json['current']
        today_date = datetime.now().strftime('%Y-%m-%d')
        
        for forecast in weather_json['forecast']['forecastday']:
            day_data = forecast['day']
            astro_data = forecast['astro']
            is_today = forecast['date'] == today_date
            
            record = {
                'snapshot_timestamp': snapshot_time,
                'city': city,
                'forecast_date': forecast['date'],
                'days_ahead': (datetime.strptime(forecast['date'], '%Y-%m-%d') - datetime.now()).days,
                'latitude': location['lat'],
                'longitude': location['lon'],
                
                # Temperature data - use current for today, avg for future days
                'temperature': current['temp_c'] if is_today else day_data['avgtemp_c'],
                'feels_like': current['feelslike_c'] if is_today else None,
                'temp_min': day_data['mintemp_c'],
                'temp_max': day_data['maxtemp_c'],
                'avg_temp': day_data['avgtemp_c'],
                
                # Weather conditions
                'weather_condition': current['condition']['text'] if is_today else day_data['condition']['text'],
                'weather_description': current['condition']['text'] if is_today else day_data['condition']['text'],
                
                # Atmospheric data - use current for today, averages for future
                'pressure': current['pressure_mb'] if is_today else None,
                'humidity': current['humidity'] if is_today else day_data['avghumidity'],
                'avg_humidity': day_data['avghumidity'],
                
                # Wind data - use current for today, max for future
                'wind_speed': (current['wind_kph'] / 3.6) if is_today else (day_data['maxwind_kph'] / 3.6),
                'wind_direction': current['wind_degree'] if is_today else None,
                'max_wind_kph': day_data['maxwind_kph'],
                
                # Cloud and visibility
                'cloudiness': current['cloud'] if is_today else None,
                'visibility': (current['vis_km'] * 1000) if is_today else (day_data['avgvis_km'] * 1000),
                'avg_visibility_km': day_data['avgvis_km'],
                
                # Precipitation
                'precip_mm': current.get('precip_mm', 0) if is_today else day_data['totalprecip_mm'],
                'total_precip_mm': day_data['totalprecip_mm'],
                'total_snow_cm': day_data.get('totalsnow_cm', 0),
                
                # UV and rain/snow chances
                'uv_index': day_data.get('uv', None),
                'daily_will_it_rain': day_data['daily_will_it_rain'],
                'daily_chance_of_rain': day_data['daily_chance_of_rain'],
                'daily_will_it_snow': day_data['daily_will_it_snow'],
                'daily_chance_of_snow': day_data['daily_chance_of_snow'],
                
                # Astronomy data
                'sunrise': astro_data['sunrise'],
                'sunset': astro_data['sunset'],
                'moonrise': astro_data['moonrise'],
                'moonset': astro_data['moonset'],
                'moon_phase': astro_data['moon_phase'],
                'moon_illumination': astro_data['moon_illumination']
            }
            
            records.append(record)
        
        return records
        
    except KeyError as e:
        print(f"Error processing data for {city}: Missing key {e}")
        return None

def save_to_excel(df, mode='append'):
    filename = 'weather_data_master.xlsx'
    filepath = os.path.join(OUTPUT_DIR, filename)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        if mode == 'append' and os.path.exists(filepath):
            existing_df = pd.read_excel(filepath)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df.to_excel(filepath, index=False)
            print(f"Appended {len(df)} records to {filepath}")
            print(f"Total records: {len(combined_df)}")
        else:
            df.to_excel(filepath, index=False)
            print(f"Created new file: {filepath}")
    except Exception as e:
        print(f"Excel Error: {e}")

def save_snapshot_backup(df):
    filename = f"weather_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join(SNAPSHOTS_DIR, filename)
    os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
    try:
        df.to_excel(filepath, index=False)
        print(f"Snapshot saved: {filepath}")
    except Exception as e:
        print(f"Snapshot Error: {e}")

def display_summary(df):
    print("\n" + "="*80)
    print("WEATHER FORECAST SUMMARY")
    print("="*80)
    
    today_df = df[df['days_ahead'] == 0]
    if len(today_df) > 0:
        print("\nTODAY'S WEATHER:")
        print(f"Temperature Range: {today_df['temp_min'].min():.1f}C to {today_df['temp_max'].max():.1f}C")
        print(f"Current Average: {today_df['temperature'].mean():.1f}C")
        warmest = today_df.loc[today_df['temperature'].idxmax()]
        coldest = today_df.loc[today_df['temperature'].idxmin()]
        print(f"Warmest: {warmest['city']} at {warmest['temperature']:.1f}C")
        print(f"Coldest: {coldest['city']} at {coldest['temperature']:.1f}C")
    
    print(f"\nFORECAST COVERAGE:")
    for day in sorted(df['days_ahead'].unique()):
        day_df = df[df['days_ahead'] == day]
        date = day_df['forecast_date'].iloc[0]
        avg_temp = day_df['avg_temp'].mean()
        rain_cities = len(day_df[day_df['daily_chance_of_rain'] > 50])
        print(f"  Day +{day} ({date}): Avg {avg_temp:.1f}C, {rain_cities} cities with >50% rain chance")
    
    print("\n" + "="*80)
    print("\nSAMPLE DATA (First 10 rows):")
    print("="*80)
    summary_df = df[['city', 'forecast_date', 'days_ahead', 'temperature', 'temp_min', 
                     'temp_max', 'humidity', 'wind_speed', 'daily_chance_of_rain']].head(10)
    summary_df = summary_df.round(1)
    print(summary_df.to_string(index=False))
    print("="*80)

def main():
    print("\n" + "="*80)
    print(f"WEATHER FORECAST PIPELINE - {FORECAST_DAYS} DAY FORECAST")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output Location: {OUTPUT_DIR}")
    print("="*80 + "\n")
    
    all_records = []
    
    for i, city in enumerate(CITIES, 1):
        print(f"[{i}/{len(CITIES)}] Fetching {FORECAST_DAYS}-day forecast for {city}...", end=" ")
        weather_data = get_weather_data(city)
        
        if weather_data:
            records = process_weather_data(weather_data, city)
            if records:
                all_records.extend(records)
                print(f"Got {len(records)} days")
            else:
                print("Processing failed")
        else:
            print("API call failed")
        
        time.sleep(0.5)
    
    if all_records:
        df = pd.DataFrame(all_records)
        print(f"\nSuccessfully processed {len(df)} forecast records")
        
        display_summary(df)
        save_to_excel(df, mode='append')
        save_snapshot_backup(df)
        
        print("\n" + "="*80)
        print("PIPELINE COMPLETE")
        print(f"Files saved to: {OUTPUT_DIR}")
        print("="*80 + "\n")
        
        return df
    else:
        print("\nNo data retrieved - pipeline failed")
        return None

if __name__ == "__main__":
    main()
