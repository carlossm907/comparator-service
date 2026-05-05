import re
import unicodedata
from typing import Optional

CANONICAL_PRODUCTS = {
    "silk_protector_solar_antiedad_fps_50": {
        "name": "SILK PROTECTOR SOLAR ANTIEDAD FPS 50" ,
        "aliases" : [
            "Silk Protector Solar Antiedad FPS 50+"
        ]
    },
    "hyalix": {
        "name": "HYALIX" ,
        "aliases" : [
            "Emulgel Medihealth Hyalix Hidratante 60 g"
        ]
    },
    "isdinceutics_hyaluronic_moisture_oily_skin_50_ml": {
        "name": "ISDINCEUTICS HYALURONIC MOISTURE OILY SKIN 50 ML." ,
        "aliases" : [
            "Crema Isdinceutics Hyaluronic Moisture Normal",
            "Isdinceutics Hyaluronic Moisture Normal 50Gr - Crema Preventiva Con Ácido Hialurónico",
            "Isdinceutics Hyaluronic Moisture Oily Skin 50 ml."
        ]
    },
    "isdin_acniben_labios": {
        "name": "ISDIN - ACNIBEN LABIOS" ,
        "aliases" : [
            "Bálsamo Renovador de Labios Isdin Acniben Repair",
            "Isdin Teen Skin RX Acniben Bálsamo Reparador Labial 10 ml.",
            "Isdin Acniben Repair Renovador Labial 10Ml."
        ]
    },
    "isdin_fusion_water_magic_alcaraz_50_ml": {
        "name": "ISDIN FUSION WATER MAGIC ALCARAZ 50 ML." ,
        "aliases" : [
            "Isdin Fusion Water Magic Alcaraz 50 ml.",
            "Fotoprotector Isdin Fusion Water Magic By Alcaraz Fps50 50Ml",
            "Fotoprotector Isdin Fusión Water Alcaraz SPF50"
        ]
    },
    "esthederm_age_proteom_advanced_serum_30ml": {
        "name": "ESTHEDERM AGE PROTEOM ADVANCED SERUM 30ML" ,
        "aliases" : [
            "Institut Esthederm Age Proteom Advanced Serum 30 ml.",
            "Age Proteom Advanced Serum 30Ml | Esthederm",
        ]
    },
    "fusion_water_magic_glow_spf": {
        "name": "FUSION WATER MAGIC GLOW SPF" ,
        "aliases" : [
            "Pack 02 Fotoprotector Isdin Fusion Water Magic Glow",
            "ISDIN Fusion Water Magic Glow SPF50 50 ml.",
            "Isdin Pack Dúo Glow"
        ]
    },
    "uriage_aguathermal_300ml": {
        "name": "URIAGE AGUATHERMAL 300ML" ,
        "aliases" : [
            "Eau Thermale Uriage Hydrates Soothes Protects",
        ]
    },
    "fusion_water_magic_spf_50": {
        "name": "FUSION WATER MAGIC SPF 50" ,
        "aliases" : [
            "Fotoprotector ISDIN Fusion Water Magic SPF50",
            "Pack 02 Fotoprotector Isdin Fusion Water Magic SPF50",
            "Pack 03 Fotoprotector Isdin Fusion Water Magic SPF50",
            "Pack Fotoprotector Isdin Fusion Water Magic + Invisible Stick",
            "Isdin Fotoprotector Fusion Water Magic SPF50 50 ml.",
            "Fotoprotector Fusion Water Magic SPF 50 - 50ml | Isdin",
            "Pack Fusion Water Magic SPF 50 | Con Color + Sin Color | Isdin",
            "Pack Fotoprotector Fusion Water Magic + FP Fusion Water Magic Color Bronze + FP Fusion Water Magic Color Medium SPF0 50ml"
        ]
    },
    "frezyderm_protector_solar_color": {
        "name": "FREZYDERM PROTECTOR SOLAR COLOR" ,
        "aliases" : [
            "Fotoprotector Frezyderm Velvet Con Color SPF50+",
            "Frezyderm Sun Screen Velvet Face SPF50+ 50 ml.",
            "Frezyderm Pack Dúo Sun Screen Velvet Con Color",
            "Fotoprotector Sun Screen Velvet con Color Face SPF50+ 50ml | Frezyderm",
            "Dúo Fotoprotector 2 Sun Screen Velvet Color | Frezyderm",
        ]
    },
    "isdinceutics_retinal_intense_50_ml": {
        "name": "ISDINCEUTICS RETINAL INTENSE 50 ML" ,
        "aliases" : [
            "Serum Isdinceutics Retinal Intense",
            "Frezyderm Sun Screen Velvet Face SPF50+ 50 ml.",
            "Isdinceutics Retinal Intense Serum 50 ml.",
            "Serum Isdinceutics Retinal Intense 50Ml | Isdin",
            "Pack Isdinceutics Retinal Intense 50ml + Fotoultra Isdin Magic Repair 50ml"
        ]
    },
    "svr_sebiaclear_ampoule_flash": {
        "name": "SVR SEBIACLEAR AMPOULE FLASH" ,
        "aliases" : [
            "SVR SEBIACLEAR AMPOULE FLASH",
        ]
    },
    "normaderm_probio-bha": {
        "name": "NORMADERM PROBIO-BHA" ,
        "aliases" : [
            "Serum Anti-imperfecciones Vichy Normaderm Probio BHA",
        ]
    },
    "alitopic_leche_emoliente_500ml": {
        "name": "ALITOPIC LECHE EMOLIENTE 500ML" ,
        "aliases" : [
            "Alitopic Leche Emoliente Emulsion",
            "Alitopic Leche Emoliente 500Ml | Carnot"
        ]
    },
    #BIODERMA PROTECTOR SOLAR
    "silk_protector_solar_antiedad_fps_50": {
        "name": "SILK PROTECTOR SOLAR ANTIEDAD FPS 50" ,
        "aliases" : [
            "Silk Protector Solar Antiedad FPS 50+",
        ]
    },
    "isdin_fotoultra_redness_spf50_50_ml": {
        "name": "ISDIN FOTOULTRA REDNESS SPF50 50 ML" ,
        "aliases" : [
            "Fotoultra Isdin Redness SPF50",
            "Isdin Fotoultra Redness SPF50 50 ml.",
            "Protector Solar FotoUltra Redness SPF 50 50ml | Isdin"
        ]
    },
    "fotoprotector_invisible_stick_spf_50": {
        "name": "FOTOPROTECTOR INVISIBLE STICK SPF 50" ,
        "aliases" : [
            "Fotoprotector Invisible Stick Isdin 50 SPF",
            "Isdin FP invisible Stick SPF50 10 gr.",
            "Fotoprotector Invisible Stick SPF 50 10g | Isdin"
        ]
    },
    "pilexil_cápsulas_50un": {
        "name": "PILEXIL CÁPSULAS 50UN" ,
        "aliases" : [
            "Pilexil Cápsulas Blandas - Caja 50 UN",
        ]
    },
    "isdinceutics_salicylic_renewal_serum_30_ml": {
        "name": "ISDINCEUTICS SALICYLIC RENEWAL SERUM 30 ML." ,
        "aliases" : [
            "Isdinceutics Salicylic Renewal Serum 30 ml.",
            "Salicilic Renewal Serum 30ml | IsdinCeutics"
        ]
    },
    "vichy_capital_soleil_uv_age_daily_spf_50_frasco_40_ml": {
        "name": "VICHY CAPITAL SOLEIL UV AGE DAILY SPF 50 - FRASCO 40 ML" ,
        "aliases" : [
            "Protector Solar Anti-Edad Vichy Capital Soleil UV Age"
        ]
    },
    #TIZO3 PRIMER SUNSCREEN CON COLOR
    "acniben_mascarilla_facial_purificante": {
        "name": "ACNIBEN MASCARILLA FACIAL PURIFICANTE" ,
        "aliases" : [
            "Isdin Acniben Mascarilla Facial Purificante 75Ml",
            "Isdin Acniben Mascarilla Facial Purificante 75 ml.",
            "Mascarilla Facial Acniben Isdin"
        ]
    },
    "hyseac_pate_sos_uriage": {
        "name": "HYSEAC PATE SOS – URIAGE" ,
        "aliases" : [
            "Crema Pàte SOS Uriage Hyséac",
        ]
    },
    "shampoo_dandrene_anti-caspa": {
        "name": "SHAMPOO DANDRENE ANTI-CASPA" ,
        "aliases" : [
            "Shampoo Dandrene Anti-caspa",
        ]
    },
    "ureadin_ultra_20-_crema_anti-rugosidades": {
        "name": "UREADIN ULTRA 20- CREMA ANTI-RUGOSIDADES" ,
        "aliases" : [
            "Crema Hidratante Ureadin Ultra 20 ISDIN",
            "Isdin Ureadin Ultra 20 Crema 100 ml.",
            "Isdin Ureadin Ultra 20 Crema anti-rugosidades 100ml"
        ]
    },
    "differin_03": {
        "name": "DIFFERIN 0.3%" ,
        "aliases" : [
            "Differin 0.3% Gel",
            "Differin 0.3% Gel Tópico - Tubo 30 G",
            "Isdin Ureadin Ultra 20 Crema anti-rugosidades 100ml"
        ]
    },
    "isdin_acniben_exfoliante_100_ml": {
        "name": "ISDIN ACNIBEN EXFOLIANTE 100 ML." ,
        "aliases" : [
            "Isdin Acniben Exfoliante 100 ml.",
            "Acniben Exfoliante Suave - Gel Exfoliante Para Piel Mixta A Grasa",
        ]
    },
    "daeha_x_30_cap": {
        "name": "DAEHA X 30 CAP" ,
        "aliases" : [
            "Daeha Capsula",
        ]
    },
    #SVR TOPIALYSE BAUME LAVANT LIMPIADOR CALMANTE 400ML
    "agua_uriage_thermale_300ml": {
        "name": "AGUA URIAGE THERMALE 300ML" ,
        "aliases" : [
            "Eau Thermale Uriage Hydrates Soothes Protects",
        ]
    },
    "neotone_radiance_color_spf_50": {
        "name": "NEOTONE RADIANCE COLOR SPF 50" ,
        "aliases" : [
            "Neotone Radiance Spf 50+ Medium",
        ]
    },
    #ACNEFREE
    "umbrella_urban_emulsión_spf50": {
        "name": "UMBRELLA URBAN EMULSIÓN SPF50" ,
        "aliases" : [
            "Umbrella Urban SPF50 50 gr.",
            "Protección Solar Umbrella Urban Emulsión SPF50"
        ]
    },
    "neotone_serum_30ml": {
        "name": "NEOTONE SERUM 30ML" ,
        "aliases" : [
            "Crema en Gel Neotone New Form",
        ]
    },
    #ISDIN AGE REPAIR COLOR
    #ISISPHARMA TEEN DERM HYDRA 40ML
    "isdinceutics_melaclear_advanced_30ml": {
        "name": "ISDINCEUTICS MELACLEAR ADVANCED 30ML" ,
        "aliases" : [
            "Serum Isdinceutics Melaclear Advanced",
            "Isdinceutics Melaclear Advanced 30 ml.",
            "New Isdinceutics Melaclear Advance 30ml",
            "Melaclear Advanced 30ml | Isdinceutics"
        ]
    },
    #SVR SEBIACLEAR GEL MOUSSANT
    #SVR TOPIALYSE CLEANSING GEL
    #UMBRELLA SPORT ACTIVE SPF50 170GR
    "isdin_acniben_spray_body": {
        "name": "ISDIN ACNIBEN SPRAY BODY" ,
        "aliases" : [
            "Reducción de Granos Corporales Acniben Body Spray",
            "Isdin Teen Skin Acniben Body 150 ml.",
            "New Isdinceutics Melaclear Advance 30ml",
            "Teen Skin Acniben Body Spray 150ml | Isdin"
        ]
    },
    "babe_hydra-calm_body_milk_500ml": {
        "name": "BABE HYDRA-CALM BODY MILK 500ML" ,
        "aliases" : [
            "Jabón Babé Hidra-Calm",
        ]
    },
    "babé_stop_akn_gel_secante_8_ml": {
        "name": "BABÉ STOP AKN GEL SECANTE 8 ML" ,
        "aliases" : [
            "Babé Stop AKN Gel Secante 8 ml.",
        ]
    },
    #TIZO MINERAL STICK TINTED SPF 45 - COLOR
    "isdinceutics_hyaluronic_moisture_sensitive_skin_50_ml": {
        "name": "ISDINCEUTICS HYALURONIC MOISTURE SENSITIVE SKIN 50 ML." ,
        "aliases" : [
            "Isdinceutics Hyaluronic Moisture Sensitive Skin 50 ml.",
            "Hyaluronic Moisture Sensitive Skin 50ml | Isdinceutics"
        ]
    },
    "bariéderm-cica_crema_con_cu-zn_40ml": {
        "name": "BARIÉDERM-CICA CREMA CON CU-ZN 40ML" ,
        "aliases" : [
            "Gel Uriage BariédermCica Daily",
        ]
    },
    "sérum_anti-manchas_la_roche_posay_mela_b3": {
        "name": "SÉRUM ANTI-MANCHAS LA ROCHE POSAY MELA B3" ,
        "aliases" : [
            "Sérum Anti-manchas La Roche-Posay Mela B3",
            "La Roche Posay Mela B3 Serum 30 ml.",
            "Mela B3 Serum 30ml | La Roche-Posay"
        ]
    },
    #MELINE 02 ETHNIC SKIN DAY 30ML
    #TIMOFREE
    "frezyderm_protector_solar": {
        "name": "FREZYDERM PROTECTOR SOLAR" ,
        "aliases" : [
            "Velvet Sunscreen Body SPF50+ 125ml | Frezyderm",
            "Frezyderm Protector Solar Velvet Stars 175 ml.",
            "Frezyderm Sun Screen Velvet Face SPF50+ 50 ml."
        ]
    },
    "vichy_capital_soleil_uv_age_daily_con_color_spf_50_frasco_40_ml": {
        "name": "VICHY CAPITAL SOLEIL UV AGE DAILY CON COLOR SPF 50 - FRASCO 40 ML" ,
        "aliases" : [
            "Protector Solar Anti-Edad Vichy Capital Soleil UV Age con Color",
        ]
    },
    "fisiogel_hipoalergénico": {
        "name": "FISIOGEL HIPOALERGÉNICO" ,
        "aliases" : [
            "Fisiogel Crema Líquida Hidratante 400ml",
        ]
    },
    #HYNDRIAX 20- ISOTRETINOINA 20MG- 10 CAPSULAS
    "nutratopic_pro-amp": {
        "name": "NUTRATOPIC PRO-AMP CR FAC.FCO X50ML" ,
        "aliases" : [
            "Crema Facial Nutratopic ProAMP Isdin",
            "Isdin Nutratopic Pro-Amp Crema Facial 50 ml.",
            "Isdin Nutratopic Pro-Amp Crema Facial 50Ml C/F - Crema Facial Protectora Reducción Signos Piel Reactiva"
        ]
    },
    "neotone_radiance_spf_50": {
        "name": "NEOTONE RADIANCE SPF 50" ,
        "aliases" : [
            "Neotone Radiance Spf 50+ Medium",
        ]
    },
    "uriage_hyseac_new-skin_serum_anti-blemish_booster_30_ml": {
        "name": "URIAGE HYSEAC NEW-SKIN SERUM ANTI-BLEMISH BOOSTER 30 ML" ,
        "aliases" : [
            "Sérum Anti-imperfecciones Uriage Hyséac",
        ]
    },
    #SVR SENSIFINE AR AGUA MICELAR - 400 ML
    #ULTRA EYE CONTOUR ESSENTIALS IT PHARMA
    "isdin_protector_solar_fusion_water_color": {
        "name": "ISDIN PROTECTOR SOLAR FUSION WATER COLOR" ,
        "aliases" : [
            "Isdin Fotoprotector Fusion Water Magic Color SPF50 50 ml.",
        ]
    },
    "protector_solar_vichy_capital_soleil_matificante_3_en_1_fps_50_-_frasco_50_ml": {
        "name": "PROTECTOR SOLAR VICHY CAPITAL SOLEIL MATIFICANTE 3 EN 1 FPS 50 - FRASCO 50 ML" ,
        "aliases" : [
            "Pack Protector Solar Matificante Vichy Capital Soleil 3 en 1 FPS50+ + Agua Solar Protectora Vichy FPS 50",
        ]
    },

}

def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_product_config(user_input: str) -> Optional[dict]:
    normalized_input = normalize_text(user_input)

    for _, data in CANONICAL_PRODUCTS.items():
        normalized_name = normalize_text(data["name"])
        if normalized_input == normalized_name:
            return data

        for alias in data["aliases"]:
            if normalized_input == normalize_text(alias):
                return data

    for _, data in CANONICAL_PRODUCTS.items():
        normalized_name = normalize_text(data["name"])
        if normalized_input in normalized_name:
            return data

        for alias in data["aliases"]:
            if normalized_input in normalize_text(alias):
                return data

    return None


def matches_alias(product_name: str, aliases: list[str]) -> bool:
    normalized_product_name = normalize_text(product_name)

    for alias in aliases:
        normalized_alias = normalize_text(alias)

        if normalized_alias in normalized_product_name:
            return True

        if normalized_product_name in normalized_alias:
            return True

    return False