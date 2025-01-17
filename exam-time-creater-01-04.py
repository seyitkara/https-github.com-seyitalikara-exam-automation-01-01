import pandas as pd
import openpyxl
from datetime import datetime, timedelta
from tkinter import Tk, simpledialog

def create_meeting_schedule(ders1, ders2, ders3, output_file):
    # Excel dosyalarını oku
    df1 = pd.read_excel(ders1)
    df2 = pd.read_excel(ders2)
    df3 = pd.read_excel(ders3)

    # Her DataFrame'e dosya adını ekle
    df1['Dosya'] = ders1
    df2['Dosya'] = ders2
    df3['Dosya'] = ders3

    # Tüm DataFrame'leri birleştir ve ortak isimleri bul
    combined_df = pd.concat([df1, df2, df3])
    common_names = combined_df['İsim'].value_counts()[combined_df['İsim'].value_counts() > 1].index.tolist()

    # Kullanıcıdan Başlangıç tarihi ve saati al
    root = Tk()
    root.withdraw()  # Pencereyi gizle
    start_time_str = simpledialog.askstring(title="Başlangıç Zamanı",
                                           prompt="Toplantıların başlangıç tarihini ve saatini YYYY-AA-GG Saat:Dakika formatında girin (örneğin: 2023-11-24 10:00):")
    root.destroy()  # Pencereyi kapat

    # Girilen değeri datetime nesnesine dönüştür
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")

    # Yeni bir Excel dosyası oluştur
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(['İsim', 'Dosya', 'Toplantı Saati'])  # Yeni sütun ekledik

    for name in common_names:
        # İsme göre filtrele
        filtered_df = combined_df[combined_df['İsim'] == name]

        # Çakışma olup olmadığını kontrol et
        if len(filtered_df) > 1:
            for index, row in filtered_df.iterrows():
                sheet.append([name, row['Dosya'], start_time.strftime("%Y-%m-%d %H:%M")])
                start_time += timedelta(hours=1)
        else:
            row = filtered_df.iloc[0]
            sheet.append([name, row['Dosya'], start_time.strftime("%Y-%m-%d %H:%M")])

    workbook.save(output_file)

# Dosya isimlerini değiştir
ders1 = "ders1.xlsx"
ders2 = "ders2.xlsx"
ders3 = "ders3.xlsx"
output_file = "toplantı_takvimi.xlsx"

create_meeting_schedule(ders1, ders2, ders3, output_file)
print("herşey başarılı")