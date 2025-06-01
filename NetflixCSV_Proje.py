import pandas as pd



df = pd.read_csv(r"C:\Users\user\Downloads\NetflixViewingHistory.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["HaftaGunu"] = df["Date"].dt.day_name()
df["Ay"]  = df["Date"].dt.month
df["Gün"] = df["Date"].dt.day

df_sezonlu = df[df["Title"].str.contains("Sezon",na = False)].copy()
df_sezonlu["Sezon"] = df_sezonlu["Title"].str.extract(r"(\d+)\. Sezon").astype("Int64")
df_sezonlu["Dizi"] = df_sezonlu["Title"].str.extract(r"^(.*?): \d+\. Sezon",expand=False).str.strip()

"""Burda Sezonlarımızın Hangi Dizileri İçerdiğini Görürüz Örneğim 1.Sezonda Alpha Male Dizisi Varken 2.Sezonda
Kullanıcının İzlenme Listesinde Olmayabilir"""
Sezon_Kapasitesi = df_sezonlu.groupby("Sezon")["Dizi"].apply(lambda x: list(set(x)))
print(Sezon_Kapasitesi)

"""Burda Kullanıcının Dizileri Kaç Farklı Günde İzlendiğini Görürüz"""
Hangi_Dizi_Kac_Gun = df_sezonlu.groupby("Dizi")["Gün"].nunique()
print(Hangi_Dizi_Kac_Gun)


"""Burda Kullanıcının İzlediği Dizilerinin En Çok İzlendiği Gün Hangisi ise Onu Görürüz"""
gunluk_izlenme = df_sezonlu.groupby(["Dizi", "HaftaGunu"]).size()
en_cok_izlenen_gun = gunluk_izlenme.groupby(level = 0).idxmax()
print(en_cok_izlenen_gun)