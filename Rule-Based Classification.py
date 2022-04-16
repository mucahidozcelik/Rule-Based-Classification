
# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama.


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# veri seti ile ilgili genel bilgileri gösteriniz.
df =pd.read_csv("persona.csv")

def hizli_bakis(dataframe):
    print("##################### Shape #####################")
    print(dataframe.shape)

    print("##################### Types #####################")
    print(dataframe.dtypes)

    print("##################### Head #####################")
    print(dataframe.head())

    print("##################### Tail #####################")
    print(dataframe.tail())

    print("##################### NA #####################")
    print(dataframe.isnull().sum())

    print("##################### Describe #####################")
    print(dataframe.describe().T)

hizli_bakis(df)

#Kaç unique SOURCE vardır? Frekansları nedir?

df["SOURCE"].nunique()


#Kaç unique PRICE vardır?

df["PRICE"].nunique()


#Hangi PRICE'dan kaçar tane satış gerçekleşmiş?

df["PRICE"].groupby(df["PRICE"]).count()

#Hangi ülkeden kaçar tane satış olmuş?

df[["COUNTRY","PRICE"]].groupby("COUNTRY").agg({"count"})

#Ülkelere göre satışlardan toplam ne kadar kazanılmış?

df[["COUNTRY","PRICE"]].groupby("COUNTRY").agg({"sum"})

#SOURCE türlerine göre göre satış sayıları nedir?

df[["SOURCE","PRICE"]].groupby("SOURCE").agg({"count"})

#Ülkelere göre PRICE ortalamaları nedir?

df[["COUNTRY","PRICE"]].groupby("COUNTRY").agg({"mean"})

#SOURCE'lara göre PRICE ortalamaları nedir?

df[["SOURCE","PRICE"]].groupby("SOURCE").agg({"mean"})

#COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?

df[["COUNTRY","SOURCE","PRICE"]].groupby(["COUNTRY","SOURCE"]).agg({"mean"})



#COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?

df[["COUNTRY","SOURCE","SEX","AGE","PRICE"]].groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"})

# or

df.pivot_table(values="PRICE", index=["COUNTRY","SOURCE","SEX","AGE"], aggfunc="mean")


#Çıktıyı PRICE’a göre sıralayınız.

agg_df = df[["COUNTRY","SOURCE","SEX","AGE","PRICE"]].groupby(["COUNTRY","SOURCE","SEX","AGE"]).\
    agg({"PRICE":"mean"}).sort_values("PRICE",ascending = False)


#Index’te yer alan isimleri değişken ismine çeviriniz.

agg_df = agg_df.reset_index()


#age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"],bins=[1,18,23,30,40,66], labels=["0_18","19_23","24_30","31_40","41_66"])


#Yeni seviye tabanlı müşterileri (persona) tanımlayınız.

a=pd.DataFrame()
a["customer_level_base"] = pd.DataFrame([row[0].upper()+"_"+row[1].upper()+"_"+row[2].upper()+"_"+row[5].upper()
                                         for row in agg_df.values])


agg_df = a.join(agg_df["PRICE"])

agg_df["customer_level_base"].nunique()

agg_df = agg_df[["customer_level_base","PRICE"]].groupby("customer_level_base").agg({"PRICE":"mean"}).sort_values("PRICE",ascending = False)

agg_df.reset_index()


#Yeni müşterileri (personaları) segmentlere ayırınız.

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D","C","B","A"])

agg_df = agg_df.reset_index()

agg_df[["customer_level_base","PRICE","SEGMENT"]].groupby(["SEGMENT","customer_level_base"]).agg({"PRICE":["mean","max","sum"]})

agg_df[agg_df["SEGMENT"] == "C"]

agg_df[agg_df["SEGMENT"] == "C"][["customer_level_base","PRICE","SEGMENT"]].agg({"PRICE":["mean","max","sum"]})


#Yeni gelen müşterileri segmentlerine göre sınıflandırınız ve ne kadar gelir getirebileceğini tahmin ediniz.

new_user = "TUR_ANDROID_FEMALE_31_40"

agg_df[agg_df["customer_level_base"] == new_user]["PRICE"]

new_user2 = "FRA_IOS_FEMALE_31_40"

agg_df[agg_df["customer_level_base"] == new_user2]["PRICE"]






