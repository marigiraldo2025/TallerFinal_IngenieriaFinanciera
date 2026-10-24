# -*- coding: utf-8 -*-
"""
Taller Final - Tablero de Visualizacion
Ingenieria Financiera - UPB
Sintesis de interes, rentabilidad, series uniformes, gradientes y amortizacion.

Ejecutar:   streamlit run app.py
"""
import math

import numpy as np
import numpy_financial as npf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# =============================================================================
# CONFIGURACION GENERAL (editar aqui los nombres del equipo)
# =============================================================================
INTEGRANTES = ["Integrante 1", "Integrante 2", "Integrante 3"]
CURSO = "Ingeniería Financiera  |  Docente: Adriana Arango L.  |  UPB"
FECHA_CONSULTA = "24 de octubre de 2026"

st.set_page_config(page_title="Tablero de Ingeniería Financiera", layout="wide",
                   initial_sidebar_state="collapsed")

# Paleta exclusivamente en azules
AZ_MARINO = "#0B2545"
AZ_OSCURO = "#13315C"
AZ_MEDIO = "#1E5AA8"
AZ_BASE = "#2E86DE"
AZ_CLARO = "#5DADE2"
AZ_CIELO = "#A9CCE3"
AZ_HIELO = "#EAF2FB"
AZ_ACERO = "#8DA9C4"
PALETA = [AZ_MEDIO, AZ_CLARO, AZ_MARINO, AZ_ACERO, AZ_BASE, AZ_CIELO, "#1B4F72", "#2874A6"]
ESCALA_AZUL = [[0, "#EAF2FB"], [0.35, "#A9CCE3"], [0.65, "#2E86DE"], [1, "#0B2545"]]

st.markdown(f"""
<style>
.stApp {{background: linear-gradient(180deg,#F3F8FE 0%, #FFFFFF 35%);}}
header[data-testid="stHeader"] {{background: transparent;}}
[data-testid="stSidebar"], [data-testid="collapsedControl"] {{display:none;}}
.block-container {{padding-top: 1.2rem; max-width: 1400px;}}
h1, h2, h3, h4 {{color:{AZ_OSCURO};}}
.hero {{background: linear-gradient(120deg,{AZ_MARINO} 0%,{AZ_OSCURO} 50%,{AZ_MEDIO} 100%);
        color:white; padding: 20px 28px; border-radius: 14px; margin-bottom: 12px;}}
.hero h1 {{color:white; font-size: 1.75rem; margin:0; padding:0;}}
.hero p {{color:#CFE2F3; margin: 4px 0 0 0; font-size: 0.95rem;}}
.equipo {{display:flex; gap:8px; flex-wrap:wrap; margin-top:12px; align-items:center;}}
.equipo span.lbl {{color:#CFE2F3; font-size:0.85rem; margin-right:4px;}}
.chip {{background: rgba(255,255,255,0.12); border:1px solid rgba(255,255,255,0.4);
        border-radius: 20px; padding: 3px 14px; font-size: 0.88rem; color:#fff;}}
.stTabs [role="tablist"] {{gap: 4px; background:{AZ_HIELO}; padding:6px; border-radius: 12px;
        flex-wrap: wrap; border-bottom:none !important;}}
.stTabs [role="tab"] {{min-height: 38px; background: white; border-radius: 8px; padding: 8px 12px;
        border:1px solid #D6E4F5 !important; color:{AZ_OSCURO} !important; font-weight:600;
        font-size:0.88rem; box-shadow:none !important;}}
.stTabs [role="tab"] * {{color:inherit !important;}}
.stTabs [role="tab"]:hover {{background:#D6E4F5;}}
.stTabs [role="tab"][aria-selected="true"] {{background:{AZ_MEDIO} !important; color:white !important;
        border-color:{AZ_MEDIO} !important;}}
.stTabs [role="tab"]::after, .stTabs [role="tab"]::before {{display:none !important;}}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{display:none;}}
.kpi {{background:white; border:1px solid #D6E4F5; border-top: 4px solid {AZ_MEDIO};
       border-radius: 12px; padding: 12px 16px; height: 100%;}}
.kpi-t {{color:#4A6A8F; font-size: 0.8rem; text-transform: uppercase; letter-spacing: .04em;}}
.kpi-v {{color:{AZ_MARINO}; font-size: 1.45rem; font-weight: 700; margin-top: 2px;}}
.kpi-s {{color:#5B7BA0; font-size: 0.8rem;}}
.caso {{background:white; border:1px solid #D6E4F5; border-radius: 14px; padding: 16px 18px;
        border-left: 6px solid {AZ_MEDIO}; height:100%;}}
.caso h4 {{margin: 0 0 6px 0; color:{AZ_MARINO};}}
.caso table {{width:100%; font-size:0.88rem;}}
.caso td {{padding: 3px 0; border:none; color:{AZ_OSCURO};}}
.caso td.v {{text-align:right; font-weight:600; color:{AZ_MARINO};}}
.decision {{background:{AZ_HIELO}; border-radius: 8px; padding: 8px 10px; margin-top: 8px;
            color:{AZ_MARINO}; font-size:0.87rem;}}
.verif-ok {{background:#E3F0FC; border:1px solid {AZ_BASE}; color:{AZ_MARINO}; border-radius:10px;
            padding:10px 14px; margin: 8px 0; font-size:0.9rem;}}
.verif-no {{background:{AZ_MARINO}; color:white; border-radius:10px; padding:10px 14px; margin: 8px 0;}}
.nota {{background:{AZ_HIELO}; border-left: 4px solid {AZ_CLARO}; border-radius:8px; padding:10px 14px;
        color:{AZ_OSCURO}; font-size:0.9rem; margin: 6px 0;}}
.seccion {{color:{AZ_OSCURO}; border-bottom: 2px solid {AZ_CIELO}; padding-bottom: 4px;
           margin-top: 14px; font-weight: 700; font-size: 1.1rem;}}
div[data-testid="stExpander"] details {{border:1px solid #D6E4F5; border-radius:10px; background:white;}}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# UTILIDADES DE FORMATO Y GRAFICOS
# =============================================================================
def cop(x, dec=0):
    """Formato pesos colombianos: $ 1.234.567"""
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "-"
    s = f"{abs(x):,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-$ " if x < 0 else "$ ") + s


def usd(x, dec=2):
    s = f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return "US$ " + s


def pct(x, dec=2):
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "-"
    return f"{x * 100:.{dec}f}".replace(".", ",") + " %"


def num(x, dec=2):
    return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def estilo(fig, titulo, xt="", yt="", h=390, leyenda=True):
    fig.update_layout(
        title=dict(text=titulo, font=dict(size=15, color=AZ_MARINO)),
        template="plotly_white", colorway=PALETA, height=h,
        margin=dict(l=10, r=10, t=50, b=10), separators=",.",
        font=dict(color=AZ_OSCURO, size=12),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F7FAFE",
        showlegend=leyenda,
        legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
        hoverlabel=dict(bgcolor="white", font_color=AZ_MARINO),
    )
    fig.update_xaxes(title=xt, gridcolor="#E1EAF5", linecolor="#C5D6EA")
    fig.update_yaxes(title=yt, gridcolor="#E1EAF5", linecolor="#C5D6EA")
    fig.update_traces(cliponaxis=False, selector=dict(type="bar"))
    if any(t.type == "pie" for t in fig.data):
        fig.update_layout(legend=dict(y=-0.05))
    return fig


def graf(fig):
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})


def tabla(df):
    st.dataframe(df, width="stretch", hide_index=True)


def tarjeta(titulo, valor, sub=""):
    return (f"<div class='kpi'><div class='kpi-t'>{titulo}</div>"
            f"<div class='kpi-v'>{valor}</div><div class='kpi-s'>{sub}</div></div>")


def fila_kpis(items):
    cols = st.columns(len(items))
    for c, (t, v, s) in zip(cols, items):
        c.markdown(tarjeta(t, v, s), unsafe_allow_html=True)


def seccion(txt):
    st.markdown(f"<div class='seccion'>{txt}</div>", unsafe_allow_html=True)


def nota(txt):
    st.markdown(f"<div class='nota'>{txt}</div>", unsafe_allow_html=True)


def verificacion(texto, ok):
    clase = "verif-ok" if ok else "verif-no"
    estado = "VERIFICACIÓN CORRECTA" if ok else "REVISAR"
    st.markdown(f"<div class='{clase}'><b>{estado}.</b> {texto}</div>", unsafe_allow_html=True)


def cerca(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# =============================================================================
# FUNCIONES FINANCIERAS
# =============================================================================
PERIODICIDADES = {"Diaria (365)": 365, "Mensual": 12, "Bimestral": 6, "Trimestral": 4,
                  "Cuatrimestral": 3, "Semestral": 2, "Anual": 1}
SIGLAS = {365: "D", 12: "M", 6: "B", 4: "T", 3: "C", 2: "S", 1: "A"}


def ea_desde(valor, forma, m, modalidad):
    """Convierte cualquier tasa a efectiva anual (vencida)."""
    ip = valor if forma == "Efectiva periódica" else valor / m
    if modalidad == "Anticipada":
        ip = ip / (1 - ip)
    return (1 + ip) ** m - 1


def periodica_desde_ea(ea, m):
    return (1 + ea) ** (1 / m) - 1


def cuota_fija(P, i, n):
    return P / n if i == 0 else P * i / (1 - (1 + i) ** -n)


def tabla_amortizacion(P, i, n, sistema):
    filas = [{"Periodo": 0, "Cuota": 0.0, "Interés": 0.0, "Abono a capital": 0.0, "Saldo": P}]
    saldo = P
    A = cuota_fija(P, i, n)
    for k in range(1, n + 1):
        interes = saldo * i
        if sistema == "Cuota fija":
            abono = A - interes
            cuota = A
        else:
            abono = P / n
            cuota = abono + interes
        saldo = saldo - abono
        if k == n:
            saldo = 0.0 if abs(saldo) < 1e-4 * max(P, 1) else saldo
        filas.append({"Periodo": k, "Cuota": cuota, "Interés": interes,
                      "Abono a capital": abono, "Saldo": saldo})
    return pd.DataFrame(filas)


def fmt_tabla_amort(df):
    out = df.copy()
    for c in ["Cuota", "Interés", "Abono a capital", "Saldo"]:
        out[c] = out[c].map(cop)
    return out


def vf_serie(A, i, n):
    return A * n if i == 0 else A * ((1 + i) ** n - 1) / i


def cuota_para_vf(F, i, n):
    return F / n if i == 0 else F * i / ((1 + i) ** n - 1)


def vp_geometrico(A1, g, i, n):
    if abs(i - g) < 1e-12:
        return n * A1 / (1 + i)
    return A1 * (1 - ((1 + g) / (1 + i)) ** n) / (i - g)


def vp_aritmetico(A1, G, i, n):
    a = (1 - (1 + i) ** -n) / i
    return A1 * a + (G / i) * (a - n / (1 + i) ** n)


# =============================================================================
# DATOS DE ENTRADA DE LOS CASOS (fuentes en la pestaña "Supuestos y fuentes")
# =============================================================================
SMMLV = 1_750_905          # SMMLV 2026 (documento VTUP CDT Nu, 06-oct-2026)
UVT = 52_374               # UVT 2026 (tarifario tarjeta Nu, oct-2026)
RANGOS = ["Hasta 2 SMMLV", "Más de 2 y hasta 4 SMMLV", "Más de 4 SMMLV"]
# FNA - crédito hipotecario en pesos, tasa E.A. por rango de ingreso (fna.gov.co/transparencia/.../tasas)
FNA_TASAS = {"Cesantías": [0.1000, 0.1210, 0.1260],
             "Ahorro Voluntario Contractual (AVC)": [0.1150, 0.1310, 0.1360]}
# Banco Caja Social - tasa promedio ponderada compra de vivienda en pesos (Superfinanciera, corte 10-jul-2026)
CAJA_TASAS = {"VIS": 0.136, "No VIS": 0.140}
# CDT Nu - tasas vigentes desde 06-oct-2026 (documento VTUP oficial)
NU_CDT = {60: 0.0945, 90: 0.0970, 120: 0.0980, 180: 0.1055, 270: 0.1075,
          360: 0.1105, 720: 0.1140, 1080: 0.1100}

D = {
    # Caso 1
    "c1_valor": 200_000_000, "c1_ingreso": 6_500_000, "c1_estado": "Nueva",
    "c1_modalidad": "Sobre planos", "c1_afiliacion": "Cesantías", "c1_joven": False,
    "c1_plazo": 20, "c1_tope_vis": 135, "c1_proy_fin": True, "c1_desc_cs": 1.0,
    "c1_ltv_fna_vis": 100, "c1_ltv_fna_novis": 90, "c1_ltv_cs_vis": 80, "c1_ltv_cs_novis": 70,
    "c1_aval_fna": 380_000, "c1_tit_fna": 250_000, "c1_aval_cs": 450_000, "c1_tit_cs": 300_000,
    "c1_notaria": 0.15, "c1_benef": 1.00, "c1_registro": 0.50,
    "c1_meses_plan": 24, "c1_tasa_ahorro": 11.25, "c1_g_plan": 5.0,
    "c1_tasa_cs_manual": 0.0, "c1_tasa_fna_manual": 0.0,
    # Caso 2
    "c2_monto": 10_000_000, "c2_dias": 360, "c2_tasa_nu_cdt": 11.05, "c2_tasa_bc_cdt": 11.66,
    "c2_tasa_nu_aho": 11.25, "c2_tasa_bc_aho": 0.05, "c2_ret_cdt": 4.0, "c2_ret_aho": 7.0,
    "c2_umbral_uvt": 0.055, "c2_aporte": 500_000, "c2_g": 5.0, "c2_meses": 36,
    # Caso 3
    "c3_inv": 10_000_000, "c3_anios": 5, "c3_trm": 3163.76, "c3_r": 10.0, "c3_dev": 3.0,
    "c3_div": 1.06, "c3_ret_div": 30.0, "c3_er": 0.03, "c3_spread_c": 1.0, "c3_spread_v": 1.0,
    "c3_comision": 0.0, "c3_aporte": 0, "c3_g_aporte": 5.0,
}


def ss(k):
    return st.session_state.get(k, D[k])


# ---------------------------- Caso 1: vivienda ------------------------------
def rango_idx(ingreso):
    s = ingreso / SMMLV
    return 0 if s <= 2 else (1 if s <= 4 else 2)


def calc_caso1(p):
    valor, ingreso = p["valor"], p["ingreso"]
    tope = p["tope_vis"] * SMMLV
    tipo = "VIS" if valor <= tope else "No VIS"
    ri = rango_idx(ingreso)
    n = int(p["plazo"] * 12)
    sobre_planos = (p["estado"] == "Nueva" and p["modalidad"] == "Sobre planos")

    t_fna = FNA_TASAS[p["afiliacion"]][ri] - (0.005 if p["joven"] else 0.0)
    if p["tasa_fna_manual"] > 0:
        t_fna = p["tasa_fna_manual"] / 100
    t_cs = CAJA_TASAS[tipo] - (p["desc_cs"] / 100 if (sobre_planos and p["proy_fin"]) else 0.0)
    if p["tasa_cs_manual"] > 0:
        t_cs = p["tasa_cs_manual"] / 100

    escr_pct = (p["notaria"] + p["benef"] + p["registro"]) / 100
    i_aho = periodica_desde_ea(p["tasa_ahorro"] / 100, 12)
    g_m = (1 + p["g_plan"] / 100) ** (1 / 12) - 1
    mp = int(p["meses_plan"])

    ent = {}
    specs = {
        "Fondo Nacional del Ahorro": dict(
            t=t_fna, ltv=(p["ltv_fna_vis"] if tipo == "VIS" else p["ltv_fna_novis"]) / 100,
            aval=0 if p["joven"] else p["aval_fna"], tit=0 if p["joven"] else p["tit_fna"]),
        "Banco Caja Social": dict(
            t=t_cs, ltv=(p["ltv_cs_vis"] if tipo == "VIS" else p["ltv_cs_novis"]) / 100,
            aval=p["aval_cs"], tit=p["tit_cs"]),
    }
    for nombre, s in specs.items():
        monto = valor * s["ltv"]
        ci = valor - monto
        im = periodica_desde_ea(s["t"], 12)
        cuota = cuota_fija(monto, im, n)
        tot_cuotas = cuota * n
        intereses = tot_cuotas - monto
        escr = valor * escr_pct
        gastos = s["aval"] + s["tit"] + escr
        tabla_df = tabla_amortizacion(monto, im, n, "Cuota fija")
        saldo_5 = float(tabla_df.loc[min(60, n), "Saldo"])
        a_unif = cuota_para_vf(ci, i_aho, mp) if ci > 0 else 0.0
        fact_g = ((1 + i_aho) ** mp - (1 + g_m) ** mp) / (i_aho - g_m) if abs(i_aho - g_m) > 1e-12 \
            else mp * (1 + i_aho) ** (mp - 1)
        a1_grad = ci / fact_g if ci > 0 else 0.0
        ent[nombre] = dict(tasa=s["t"], im=im, nominal_mv=im * 12, ltv=s["ltv"], monto=monto, ci=ci,
                           cuota=cuota, tot_cuotas=tot_cuotas, intereses=intereses,
                           avaluo=s["aval"], titulos=s["tit"], escrituracion=escr, gastos=gastos,
                           total=ci + tot_cuotas + gastos, costo_fin=intereses + gastos,
                           rel=cuota / ingreso, cumple=cuota / ingreso <= 0.30, tabla=tabla_df,
                           saldo_5=saldo_5, a_unif=a_unif, a1_grad=a1_grad)
    # Comparación justa: ambas entidades sobre el mismo monto financiado
    monto_c = min(v["monto"] for v in ent.values())
    for v in ent.values():
        cuota_c = cuota_fija(monto_c, v["im"], n)
        v["monto_c"] = monto_c
        v["cuota_c"] = cuota_c
        v["int_c"] = cuota_c * n - monto_c
        v["costo_c"] = v["int_c"] + v["gastos"]
        v["rel_c"] = cuota_c / ingreso
    elegibles = {k: v for k, v in ent.items() if v["rel_c"] <= 0.30} or ent
    mejor = min(elegibles, key=lambda k: elegibles[k]["costo_c"])
    return dict(tipo=tipo, rango=RANGOS[ri], n=n, ent=ent, mejor=mejor, sobre_planos=sobre_planos,
                tope=tope, i_aho=i_aho, g_m=g_m, mp=mp)


def params_c1():
    return {k[3:]: ss(k) for k in D if k.startswith("c1_")}


# ---------------------------- Caso 2: CDT vs ahorro --------------------------
def crecimiento_cuenta(monto, ea, dias, ret, umbral):
    """Capitalización diaria; retención si el rendimiento diario supera el umbral."""
    i_d = (1 + ea) ** (1 / 365) - 1
    saldo = monto
    tray = [saldo]
    ret_total = 0.0
    for _ in range(int(dias)):
        int_d = saldo * i_d
        r = int_d * ret if int_d > umbral else 0.0
        ret_total += r
        saldo += int_d - r
        tray.append(saldo)
    return np.array(tray), ret_total


def calc_caso2(p):
    monto, dias = p["monto"], int(p["dias"])
    umbral = p["umbral_uvt"] * UVT
    res = {}
    for nombre, ea in [("CDT Nu", p["tasa_nu_cdt"] / 100), ("CDT Bancolombia", p["tasa_bc_cdt"] / 100)]:
        bruto = monto * ((1 + ea) ** (dias / 365) - 1)
        ret = bruto * p["ret_cdt"] / 100
        neto = bruto - ret
        ea_neta = (1 + neto / monto) ** (365 / dias) - 1
        t = np.arange(dias + 1)
        tray = monto * (1 + ea) ** (t / 365)
        res[nombre] = dict(tipo="CDT", ea=ea, bruto=bruto, ret=ret, neto=neto, final=monto + neto,
                           ea_neta=ea_neta, tray=tray)
    for nombre, ea in [("Cuenta Nu (Cajitas)", p["tasa_nu_aho"] / 100),
                       ("Cuenta de ahorros Bancolombia", p["tasa_bc_aho"] / 100)]:
        tray, ret = crecimiento_cuenta(monto, ea, dias, p["ret_aho"] / 100, umbral)
        final = tray[-1]
        neto = final - monto
        ea_neta = (final / monto) ** (365 / dias) - 1
        res[nombre] = dict(tipo="Ahorro", ea=ea, bruto=neto + ret, ret=ret, neto=neto, final=final,
                           ea_neta=ea_neta, tray=tray)
    mejor = max(res, key=lambda k: res[k]["final"])
    # plan de ahorro (series y gradiente) en cuentas
    n = int(p["meses"])
    g_m = (1 + p["g"] / 100) ** (1 / 12) - 1
    plan = {}
    for nombre in ["Cuenta Nu (Cajitas)", "Cuenta de ahorros Bancolombia"]:
        i_m = periodica_desde_ea(res[nombre]["ea"], 12)
        uni, gra, ap_u, ap_g = [0.0], [0.0], [0.0], [0.0]
        for k in range(1, n + 1):
            a_g = p["aporte"] * (1 + g_m) ** (k - 1)
            uni.append(uni[-1] * (1 + i_m) + p["aporte"])
            gra.append(gra[-1] * (1 + i_m) + a_g)
            ap_u.append(ap_u[-1] + p["aporte"])
            ap_g.append(ap_g[-1] + a_g)
        plan[nombre] = dict(i_m=i_m, uni=np.array(uni), gra=np.array(gra), ap_u=np.array(ap_u),
                            ap_g=np.array(ap_g))
    return dict(res=res, mejor=mejor, plan=plan, g_m=g_m, n=n, umbral=umbral)


def params_c2():
    return {k[3:]: ss(k) for k in D if k.startswith("c2_")}


# ---------------------------- Caso 3: VOO -----------------------------------
def simular_voo(p, r=None, dev=None, spread_c=None, er=None, div=None, aporte=None):
    r = p["r"] / 100 if r is None else r
    dev = p["dev"] / 100 if dev is None else dev
    spread_c = p["spread_c"] / 100 if spread_c is None else spread_c
    spread_v = p["spread_v"] / 100
    er = p["er"] / 100 if er is None else er
    div = p["div"] / 100 if div is None else div
    aporte = p["aporte"] if aporte is None else aporte
    n = int(p["anios"] * 12)
    r_m = (1 + r) ** (1 / 12) - 1
    d_m = div / 12 * (1 - p["ret_div"] / 100)
    g_m = (1 + p["g_aporte"] / 100) ** (1 / 12) - 1
    trm0 = p["trm"]
    usd_ = max(p["inv"] * (1 - spread_c) / trm0 - p["comision"], 0)
    flujos = [-p["inv"]]
    tray_usd, tray_cop, aport_acum, trm_t = [usd_], [usd_ * trm0], [p["inv"]], [trm0]
    costos_cop = p["inv"] * spread_c + p["comision"] * trm0
    for k in range(1, n + 1):
        trm_k = trm0 * (1 + dev) ** (k / 12)
        usd_ *= (1 + r_m) * (1 + d_m - er / 12)
        a_k = aporte * (1 + g_m) ** (k - 1) if aporte > 0 else 0.0
        if a_k > 0:
            usd_ += a_k * (1 - spread_c) / trm_k - p["comision"]
            costos_cop += a_k * spread_c + p["comision"] * trm_k
        flujos.append(-a_k)
        tray_usd.append(usd_)
        tray_cop.append(usd_ * trm_k)
        aport_acum.append(aport_acum[-1] + a_k)
        trm_t.append(trm_k)
    trm_n = trm_t[-1]
    final_cop = usd_ * trm_n * (1 - spread_v) - p["comision"] * trm_n
    costos_cop += usd_ * trm_n * spread_v + p["comision"] * trm_n
    flujos[-1] += final_cop
    irr_m = npf.irr(flujos)
    ea_neta = (1 + irr_m) ** 12 - 1 if irr_m is not None and not np.isnan(irr_m) else np.nan
    total_aportado = aport_acum[-1]
    return dict(final_cop=final_cop, final_usd=usd_, ea_neta=ea_neta, total_aportado=total_aportado,
                ganancia=final_cop - total_aportado, tray_usd=np.array(tray_usd),
                tray_cop=np.array(tray_cop), aport=np.array(aport_acum), trm=np.array(trm_t),
                trm_n=trm_n, costos=costos_cop, combinada=(1 + r) * (1 + dev) - 1, n=n)


def params_c3():
    return {k[3:]: ss(k) for k in D if k.startswith("c3_")}


# =============================================================================
# ENCABEZADO Y NAVEGACION SUPERIOR
# =============================================================================
chips = "".join(f"<span class='chip'>{n}</span>" for n in INTEGRANTES)
st.markdown(f"""
<div class='hero'>
  <h1>Tablero de Ingeniería Financiera</h1>
  <p>Síntesis de interés simple y compuesto, equivalencia de tasas, series uniformes, gradientes y amortización
  aplicada a tres casos reales en pesos colombianos.</p>
  <p style='font-size:0.85rem'>{CURSO}  |  Datos consultados el {FECHA_CONSULTA}</p>
  <div class='equipo'><span class='lbl'>Integrantes:</span>{chips}</div>
</div>
""", unsafe_allow_html=True)

TABS = st.tabs(["Panel principal", "Interés simple", "Interés compuesto", "Tasas y rentabilidad",
                "Series uniformes", "Gradientes", "Amortización", "Caso 1: Vivienda",
                "Caso 2: CDT vs ahorro", "Caso 3: ETF VOO", "Supuestos y fuentes"])

# =============================================================================
# PANEL PRINCIPAL
# =============================================================================
with TABS[0]:
    c1 = calc_caso1(params_c1())
    c2 = calc_caso2(params_c2())
    p3 = params_c3()
    c3 = simular_voo(p3)
    m1 = c1["ent"][c1["mejor"]]
    m2 = c2["res"][c2["mejor"]]
    cdt_nu_neta = c2["res"]["CDT Nu"]["ea_neta"]
    voo_gana = c3["ea_neta"] > cdt_nu_neta

    st.markdown("### Indicadores clave")
    fila_kpis([
        ("Tasa E.A. crédito recomendado", pct(m1["tasa"]), c1["mejor"]),
        ("Cuota mensual", cop(m1["cuota"]), f"{c1['n']} cuotas, sistema cuota fija"),
        ("Intereses totales del crédito", cop(m1["intereses"]), f"sobre un préstamo de {cop(m1['monto'])}"),
        ("Saldo del crédito al año 5", cop(m1["saldo_5"]), f"{pct(m1['saldo_5'] / m1['monto'], 1)} del capital"),
    ])
    st.write("")
    fila_kpis([
        ("Mejor alternativa de ahorro", c2["mejor"], f"plazo de {int(ss('c2_dias'))} días"),
        ("E.A. neta de retención", pct(m2["ea_neta"]), f"recibe {cop(m2['final'])}"),
        ("Valor futuro VOO (escenario base)", cop(c3["final_cop"]), f"a {int(p3['anios'])} años"),
        ("E.A. neta VOO en pesos", pct(c3["ea_neta"]), "después de costos y tasa de cambio"),
    ])

    st.markdown("### Resumen de los casos aplicados")
    cc = st.columns(3)
    otro = [k for k in c1["ent"] if k != c1["mejor"]][0]
    dif = c1["ent"][otro]["costo_c"] - m1["costo_c"]
    casos_html = [
        ("Caso 1. Crédito de vivienda", [
            ("Producto", f"Crédito hipotecario {c1['tipo']} en pesos"),
            ("Entidad recomendada", c1["mejor"]),
            ("Tasa efectiva anual", pct(m1["tasa"])),
            ("Total pagado (cuotas + inicial + gastos)", cop(m1["total"])),
            ("Intereses + gastos (monto igual)", cop(m1["costo_c"])),
        ], f"Tomar el crédito con <b>{c1['mejor']}</b>: por el mismo monto ({cop(m1['monto_c'])}) ahorra "
           f"{cop(dif)} frente a {otro} en intereses y gastos; con su oferta la cuota es el "
           f"{pct(m1['rel'], 1)} del ingreso ({'cumple' if m1['cumple'] else 'no cumple'} el tope del 30 %)."),
        ("Caso 2. CDT vs cuenta de ahorros", [
            ("Inversión", f"{cop(ss('c2_monto'))} por {int(ss('c2_dias'))} días"),
            ("Producto recomendado", c2["mejor"]),
            ("Tasa efectiva anual (bruta)", pct(m2["ea"])),
            ("E.A. neta de retención", pct(m2["ea_neta"])),
            ("Total recibido al final", cop(m2["final"])),
        ], f"Invertir en <b>{c2['mejor']}</b>. La cuenta de Bancolombia ({pct(ss('c2_tasa_bc_aho') / 100)}) "
           f"prácticamente no rinde; la Cajita Nu conviene sólo si se necesita liquidez diaria."),
        ("Caso 3. ETF Vanguard S&P 500 (VOO)", [
            ("Inversión", f"{cop(p3['inv'])} a {int(p3['anios'])} años"),
            ("Tasa combinada (rend. USD y devaluación)", pct(c3["combinada"])),
            ("E.A. neta en pesos", pct(c3["ea_neta"])),
            ("Total recibido (escenario base)", cop(c3["final_cop"])),
            ("Costos totales (cambio y comisiones)", cop(c3["costos"])),
        ], (f"<b>Invertir en VOO</b> si el horizonte es de largo plazo y se tolera la volatilidad: su E.A. neta "
            f"supera al CDT Nu ({pct(cdt_nu_neta)})." if voo_gana else
            f"<b>Preferir el CDT</b>: en este escenario VOO rinde menos que el CDT Nu neto ({pct(cdt_nu_neta)}).")),
    ]
    for col, (tit, filas, dec) in zip(cc, casos_html):
        rows = "".join(f"<tr><td>{a}</td><td class='v'>{b}</td></tr>" for a, b in filas)
        col.markdown(f"<div class='caso'><h4>{tit}</h4><table>{rows}</table>"
                     f"<div class='decision'><b>Decisión:</b> {dec}</div></div>", unsafe_allow_html=True)

    st.markdown("### Relación entre tasas")
    g1, g2 = st.columns([1.4, 1])
    with g1:
        prods = [("Crédito FNA", c1["ent"]["Fondo Nacional del Ahorro"]["tasa"], "Costo de crédito"),
                 ("Crédito Caja Social", c1["ent"]["Banco Caja Social"]["tasa"], "Costo de crédito"),
                 ("VOO (E.A. neta en COP)", c3["ea_neta"], "Rentabilidad neta"),
                 ("CDT Bancolombia (neta)", c2["res"]["CDT Bancolombia"]["ea_neta"], "Rentabilidad neta"),
                 ("CDT Nu (neta)", c2["res"]["CDT Nu"]["ea_neta"], "Rentabilidad neta"),
                 ("Cajitas Nu (neta)", c2["res"]["Cuenta Nu (Cajitas)"]["ea_neta"], "Rentabilidad neta"),
                 ("Ahorros Bancolombia (neta)", c2["res"]["Cuenta de ahorros Bancolombia"]["ea_neta"],
                  "Rentabilidad neta")]
        dfp = pd.DataFrame(prods, columns=["Producto", "EA", "Tipo"]).sort_values("EA")
        fig = go.Figure()
        for tipo, color in [("Costo de crédito", AZ_MARINO), ("Rentabilidad neta", AZ_CLARO)]:
            d = dfp[dfp["Tipo"] == tipo]
            fig.add_bar(y=d["Producto"], x=d["EA"] * 100, orientation="h", name=tipo, marker_color=color,
                        text=[pct(v) for v in d["EA"]], textposition="outside")
        estilo(fig, "Tasa efectiva anual de cada producto analizado", "Tasa efectiva anual (%)", "", h=400)
        fig.update_layout(barmode="overlay")
        graf(fig)
    with g2:
        fig = go.Figure(go.Pie(labels=["Capital prestado", "Intereses", "Cuota inicial", "Gastos de trámite"],
                               values=[m1["monto"], m1["intereses"], m1["ci"], m1["gastos"]], hole=0.55,
                               marker=dict(colors=[AZ_MEDIO, AZ_MARINO, AZ_CIELO, AZ_CLARO]),
                               textinfo="percent"))
        fig.add_annotation(text=f"Total<br><b>{cop(m1['total'] / 1e6, 0)} M</b>", showarrow=False,
                           font=dict(size=14, color=AZ_MARINO))
        estilo(fig, f"Composición del total pagado ({c1['mejor']})", h=400)
        graf(fig)

    anios = int(p3["anios"])
    meses = np.arange(anios * 12 + 1)
    base = p3["inv"]
    fig = go.Figure()
    series_crec = [
        ("VOO escenario base (neto en COP)", c3["ea_neta"]),
        ("CDT Nu renovado (neto)", cdt_nu_neta),
        ("CDT Bancolombia renovado (neto)", c2["res"]["CDT Bancolombia"]["ea_neta"]),
        ("Cajitas Nu (neto)", c2["res"]["Cuenta Nu (Cajitas)"]["ea_neta"]),
        ("Ahorros Bancolombia", c2["res"]["Cuenta de ahorros Bancolombia"]["ea_neta"]),
    ]
    for (nom, ea), dash in zip(series_crec, ["solid", "dash", "dot", "dashdot", "longdash"]):
        fig.add_scatter(x=meses, y=base * (1 + ea) ** (meses / 12), name=nom, mode="lines",
                        line=dict(dash=dash, width=2.5))
    estilo(fig, f"Crecimiento de {cop(base)} según la tasa efectiva anual neta de cada alternativa",
           "Mes", "Valor acumulado (COP)", h=420)
    graf(fig)
    nota("Las cifras del panel se recalculan con los parámetros que se modifiquen dentro de cada caso aplicado. "
         "La navegación entre módulos está en las pestañas superiores.")

# =============================================================================
# MODULO 1: INTERES SIMPLE
# =============================================================================
with TABS[1]:
    st.markdown("## Módulo de interés simple")
    ce, cr = st.columns([1, 2])
    with ce:
        seccion("Parámetros de entrada")
        P = st.number_input("Capital inicial P (COP)", min_value=0, value=5_000_000, step=500_000, key="s_P")
        tasa = st.slider("Tasa de interés (%)", 0.0, 40.0, 12.0, 0.1, key="s_i") / 100
        unidad_t = st.selectbox("La tasa es", ["Anual", "Mensual", "Diaria"], key="s_ut")
        plazo = st.number_input("Plazo", min_value=1, value=180, step=1, key="s_n")
        unidad_n = st.selectbox("Unidad del plazo", ["Días", "Meses", "Años"], key="s_un")
        conv = st.radio("Convención de días", ["Comercial (año de 360 días)", "Real (año de 365 días)"],
                        key="s_conv")
        base = 360 if conv.startswith("Comercial") else 365
        F_obj = st.number_input("Valor futuro objetivo para despejes y valor presente (COP)", min_value=0,
                                value=5_500_000, step=100_000, key="s_F")
    i_anual = tasa if unidad_t == "Anual" else (tasa * 12 if unidad_t == "Mensual" else tasa * base)
    t_anios = plazo / base if unidad_n == "Días" else (plazo / 12 if unidad_n == "Meses" else plazo)
    I = P * i_anual * t_anios
    F = P + I
    VP = F_obj / (1 + i_anual * t_anios)
    i_desp = (F_obj / P - 1) / t_anios if P > 0 and t_anios > 0 else np.nan
    t_desp = (F_obj / P - 1) / i_anual if P > 0 and i_anual > 0 else np.nan
    with cr:
        seccion("Fórmulas")
        st.latex(r"I = P\cdot i\cdot t \qquad F = P\,(1+i\,t) \qquad P=\frac{F}{1+i\,t}")
        st.latex(r"i=\frac{F/P-1}{t}\qquad t=\frac{F/P-1}{i}\qquad t_{años}=\frac{días}{360\ \text{o}\ 365}")
        seccion("Resultados")
        fila_kpis([("Interés", cop(I), f"tasa anual equivalente {pct(i_anual)}"),
                   ("Valor futuro F", cop(F), f"t = {num(t_anios, 4)} años"),
                   ("Valor presente de F objetivo", cop(VP), "descontado a interés simple")])
        st.write("")
        fila_kpis([("Tasa necesaria para F objetivo", pct(i_desp) + " anual", "despeje de la tasa"),
                   ("Plazo necesario para F objetivo",
                    f"{num(t_desp, 3)} años" if not np.isnan(t_desp) else "-",
                    f"{num(t_desp * base, 0)} días" if not np.isnan(t_desp) else ""),
                   ("Convención usada", f"{base} días", conv.split(" (")[0])])
    pasos = 24
    t_grid = np.linspace(0, t_anios, pasos + 1)
    c_a, c_b = st.columns(2)
    with c_a:
        fig = go.Figure()
        fig.add_scatter(x=t_grid * 12, y=P * (1 + i_anual * t_grid), mode="lines+markers", name="Valor acumulado",
                        line=dict(color=AZ_MEDIO, width=3), fill="tozeroy", fillcolor="rgba(46,134,222,0.12)")
        fig.add_hline(y=P, line_dash="dot", line_color=AZ_MARINO, annotation_text="Capital")
        estilo(fig, "Evolución del valor acumulado (interés simple)", "Tiempo (meses)", "Valor (COP)")
        graf(fig)
    with c_b:
        dias_tot = t_anios * base
        conv_df = pd.DataFrame({"Convención": ["Comercial 360", "Real 365"],
                                "Interés": [P * i_anual * dias_tot / 360, P * i_anual * dias_tot / 365]})
        fig = go.Figure(go.Bar(x=conv_df["Convención"], y=conv_df["Interés"],
                               marker_color=[AZ_MARINO, AZ_CLARO], text=[cop(v) for v in conv_df["Interés"]],
                               textposition="outside"))
        estilo(fig, f"Interés de {num(dias_tot, 0)} días según la convención", "", "Interés (COP)", leyenda=False)
        graf(fig)
    # verificacion: suma de intereses diarios
    dias_int = int(round(t_anios * base))
    suma_diaria = sum(P * i_anual / base for _ in range(dias_int))
    verificacion(f"Suma manual de {dias_int} intereses diarios = {cop(suma_diaria)}; fórmula I = P·i·t = {cop(I)}.",
                 cerca(suma_diaria, P * i_anual * dias_int / base))

# =============================================================================
# MODULO 2: INTERES COMPUESTO
# =============================================================================
with TABS[2]:
    st.markdown("## Módulo de interés compuesto")
    ce, cr = st.columns([1, 2])
    with ce:
        seccion("Parámetros de entrada")
        Pc = st.number_input("Capital inicial P (COP)", min_value=0, value=5_000_000, step=500_000, key="c_P")
        ic = st.slider("Tasa periódica i (%)", 0.0, 10.0, 1.2, 0.01, key="c_i") / 100
        per_c = st.selectbox("Periodicidad de la tasa", list(PERIODICIDADES)[1:], key="c_per")
        nc = st.slider("Número de periodos n", 1, 360, 36, key="c_n")
        Fc_obj = st.number_input("Valor futuro objetivo para despejes (COP)", min_value=0, value=8_000_000,
                                 step=100_000, key="c_F")
    Fc = Pc * (1 + ic) ** nc
    VPc = Fc_obj / (1 + ic) ** nc
    ic_desp = (Fc_obj / Pc) ** (1 / nc) - 1 if Pc > 0 else np.nan
    nc_desp = math.log(Fc_obj / Pc) / math.log(1 + ic) if Pc > 0 and ic > 0 and Fc_obj > 0 else np.nan
    Fs = Pc * (1 + ic * nc)
    with cr:
        seccion("Fórmulas")
        st.latex(r"F=P(1+i)^n \qquad P=\frac{F}{(1+i)^n}\qquad i=\left(\frac{F}{P}\right)^{1/n}-1"
                 r"\qquad n=\frac{\ln(F/P)}{\ln(1+i)}")
        seccion("Resultados")
        fila_kpis([("Valor futuro compuesto", cop(Fc), f"{nc} periodos {per_c.lower()}es"),
                   ("Valor futuro simple (mismos datos)", cop(Fs), "comparación"),
                   ("Diferencia al final", cop(Fc - Fs), "interés sobre intereses")])
        st.write("")
        fila_kpis([("Valor presente de F objetivo", cop(VPc), ""),
                   ("Tasa periódica necesaria", pct(ic_desp, 4), f"E.A. {pct((1 + ic_desp) ** PERIODICIDADES[per_c] - 1)}"),
                   ("Periodos necesarios", num(nc_desp, 2) if not np.isnan(nc_desp) else "-", "despeje de n")])
    k = np.arange(nc + 1)
    comp = Pc * (1 + ic) ** k
    simp = Pc * (1 + ic * k)
    c_a, c_b = st.columns(2)
    with c_a:
        fig = go.Figure()
        fig.add_scatter(x=k, y=comp, name="Interés compuesto", line=dict(color=AZ_MEDIO, width=3))
        fig.add_scatter(x=k, y=simp, name="Interés simple", line=dict(color=AZ_ACERO, width=3, dash="dash"))
        estilo(fig, "Interés simple vs interés compuesto con los mismos datos", "Periodo", "Valor (COP)")
        graf(fig)
    with c_b:
        fig = go.Figure(go.Bar(x=k, y=comp - simp, marker=dict(color=comp - simp, colorscale=ESCALA_AZUL)))
        estilo(fig, "Diferencia acumulada: compuesto menos simple", "Periodo", "Diferencia (COP)", leyenda=False)
        graf(fig)
    f_npf = npf.fv(ic, nc, 0, -Pc)
    verificacion(f"numpy_financial.fv = {cop(f_npf, 2)}; fórmula P(1+i)^n = {cop(Fc, 2)}.", cerca(f_npf, Fc))

# =============================================================================
# MODULO 3: RENTABILIDAD Y EQUIVALENCIA DE TASAS
# =============================================================================
with TABS[3]:
    st.markdown("## Módulo de rentabilidad y equivalencia de tasas")
    ce, cr = st.columns([1, 2])
    with ce:
        seccion("Tasa de entrada")
        val = st.number_input("Valor de la tasa (%)", min_value=0.0, max_value=200.0, value=12.0, step=0.1,
                              key="t_val") / 100
        forma = st.radio("Tipo de tasa", ["Nominal", "Efectiva periódica"], key="t_forma", horizontal=True)
        per_t = st.selectbox("Periodicidad", list(PERIODICIDADES), index=1, key="t_per")
        modal = st.radio("Modalidad", ["Vencida", "Anticipada"], key="t_mod", horizontal=True)
        if forma == "Efectiva periódica" and per_t == "Anual" and modal == "Vencida":
            nota("Ingresó directamente una tasa efectiva anual.")
    m_t = PERIODICIDADES[per_t]
    EA = ea_desde(val, forma, m_t, modal)
    with cr:
        seccion("Fórmulas")
        st.latex(r"i_p=\frac{j}{m}\qquad EA=(1+i_p)^m-1\qquad i_p=(1+EA)^{1/m}-1")
        st.latex(r"i_v=\frac{i_a}{1-i_a}\qquad i_a=\frac{i_v}{1+i_v}\qquad "
                 r"i_{comb}=(1+i_1)(1+i_2)-1\qquad EA_{neta}=\left(1+i_p(1-r)\right)^m-1")
        fila_kpis([("Tasa efectiva anual equivalente", pct(EA, 4), f"desde {pct(val)} {forma.lower()} "
                    f"{per_t.lower()} {modal.lower()}")])
    seccion("Tabla de equivalencias (se recalcula al cambiar la tasa de entrada)")
    filas = []
    for nombre, m in PERIODICIDADES.items():
        ipv = periodica_desde_ea(EA, m)
        ipa = ipv / (1 + ipv)
        filas.append({"Periodicidad": nombre, "m": m, "Periódica vencida": ipv, "Periódica anticipada": ipa,
                      "Nominal vencida": ipv * m, "Nominal anticipada": ipa * m, "Efectiva anual": (1 + ipv) ** m - 1})
    df_eq = pd.DataFrame(filas)
    df_show = df_eq.copy()
    for c in df_show.columns[2:]:
        df_show[c] = df_show[c].map(lambda v: pct(v, 4))
    df_show["Nominal vencida"] = [f"{v} N{SIGLAS[m]}V" for v, m in zip(df_show["Nominal vencida"], df_eq["m"])]
    df_show["Nominal anticipada"] = [f"{v} N{SIGLAS[m]}A" for v, m in zip(df_show["Nominal anticipada"], df_eq["m"])]
    tabla(df_show)
    c_a, c_b = st.columns(2)
    with c_a:
        fig = go.Figure()
        fig.add_bar(x=df_eq["Periodicidad"], y=df_eq["Nominal vencida"] * 100, name="Nominal vencida",
                    marker_color=AZ_MEDIO)
        fig.add_bar(x=df_eq["Periodicidad"], y=df_eq["Nominal anticipada"] * 100, name="Nominal anticipada",
                    marker_color=AZ_CIELO)
        fig.add_hline(y=EA * 100, line_dash="dash", line_color=AZ_MARINO, annotation_text=f"E.A. {pct(EA)}")
        estilo(fig, "Tasas nominales equivalentes a la misma E.A.", "Periodicidad", "Tasa nominal anual (%)")
        fig.update_layout(barmode="group")
        graf(fig)
    with c_b:
        nominales = np.arange(4, 31, 2) / 100
        z = [[((1 + j / m) ** m - 1) * 100 for j in nominales] for m in PERIODICIDADES.values()]
        fig = go.Figure(go.Heatmap(z=z, x=[pct(j, 0) for j in nominales], y=list(PERIODICIDADES),
                                   colorscale=ESCALA_AZUL, colorbar=dict(title="E.A. %"),
                                   hovertemplate="Nominal %{x}<br>%{y}<br>E.A. %{z:.2f} %<extra></extra>"))
        estilo(fig, "Mapa de calor: E.A. según tasa nominal vencida y capitalización", "Tasa nominal",
               "Capitalización", leyenda=False)
        graf(fig)

    seccion("Tasas combinadas y rentabilidad neta con retención en la fuente")
    k1, k2, k3 = st.columns(3)
    with k1:
        infl = st.slider("Inflación anual (IPC, %)", 0.0, 15.0, 6.24, 0.01, key="t_inf") / 100
        spread = st.slider("Puntos adicionales (%)", 0.0, 10.0, 4.0, 0.05, key="t_spread") / 100
    with k2:
        ea_r = st.slider("Tasa E.A. bruta del producto (%)", 0.0, 25.0, 11.05, 0.05, key="t_ear") / 100
        ret = st.slider("Retención en la fuente sobre rendimientos (%)", 0.0, 20.0, 4.0, 0.5, key="t_ret") / 100
    with k3:
        per_pago = st.selectbox("Periodicidad de pago de intereses", list(PERIODICIDADES)[1:], index=5,
                                key="t_perpago")
    comb = (1 + infl) * (1 + spread) - 1
    m_p = PERIODICIDADES[per_pago]
    ip_b = periodica_desde_ea(ea_r, m_p)
    ea_neta = (1 + ip_b * (1 - ret)) ** m_p - 1
    fila_kpis([("Tasa combinada IPC + puntos", pct(comb, 3), f"suma simple: {pct(infl + spread, 3)}"),
               ("Tasa periódica bruta", pct(ip_b, 4), per_pago),
               ("E.A. neta de retención", pct(ea_neta, 3), f"pierde {pct(ea_r - ea_neta, 3)}")])
    c_a, c_b = st.columns(2)
    with c_a:
        fig = go.Figure(go.Waterfall(
            x=["E.A. bruta", "Retención", "E.A. neta"], measure=["absolute", "relative", "total"],
            y=[ea_r * 100, -(ea_r - ea_neta) * 100, 0], text=[pct(ea_r), "-" + pct(ea_r - ea_neta), pct(ea_neta)],
            textposition="outside", decreasing=dict(marker_color=AZ_ACERO),
            increasing=dict(marker_color=AZ_MEDIO), totals=dict(marker_color=AZ_MARINO),
            connector=dict(line=dict(color=AZ_CIELO))))
        estilo(fig, "Cascada: de la tasa bruta a la tasa neta", "", "Tasa (%)", leyenda=False)
        graf(fig)
    with c_b:
        fig = go.Figure(go.Bar(x=["Inflación", "Puntos adicionales", "Efecto cruzado", "Tasa combinada"],
                               y=[infl * 100, spread * 100, infl * spread * 100, comb * 100],
                               marker_color=[AZ_CIELO, AZ_CLARO, AZ_ACERO, AZ_MARINO],
                               text=[pct(v, 3) for v in [infl, spread, infl * spread, comb]],
                               textposition="outside"))
        estilo(fig, "Descomposición de la tasa combinada", "", "Tasa (%)", leyenda=False)
        graf(fig)
    vuelta = (1 + periodica_desde_ea(EA, 12)) ** 12 - 1
    ant_check = (val / m_t if forma == "Nominal" else val)
    verificacion(f"E.A. → mensual → E.A. devuelve {pct(vuelta, 6)} (entrada {pct(EA, 6)}). "
                 f"Para la tasa combinada: (1+{pct(infl)})(1+{pct(spread)})−1 = {pct(comb, 4)}.",
                 cerca(vuelta, EA))

# =============================================================================
# MODULO 4: SERIES UNIFORMES
# =============================================================================
with TABS[4]:
    st.markdown("## Módulo de series uniformes")
    ce, cr = st.columns([1, 2])
    with ce:
        seccion("Parámetros de entrada")
        dato = st.radio("Dato conocido", ["Cuota A", "Valor presente P", "Valor futuro F"], key="u_dato")
        valor_u = st.number_input("Valor del dato conocido (COP)", min_value=0, value=500_000, step=50_000,
                                  key="u_val")
        iu = st.slider("Tasa periódica i (%)", 0.01, 5.0, 0.9, 0.01, key="u_i") / 100
        nu = st.slider("Número de periodos n", 1, 240, 36, key="u_n")
        ku = st.slider("Periodos de gracia (serie diferida)", 0, 36, 6, key="u_k")
        tipo_g = st.radio("Tipo de serie a graficar", ["Vencida", "Anticipada"], horizontal=True, key="u_tipo")
    an = (1 - (1 + iu) ** -nu) / iu
    sn = ((1 + iu) ** nu - 1) / iu
    if dato == "Cuota A":
        A = valor_u
    elif dato == "Valor presente P":
        A = valor_u / an
    else:
        A = valor_u / sn
    Pv, Fv = A * an, A * sn
    Pa, Fa = Pv * (1 + iu), Fv * (1 + iu)
    Pd = Pv / (1 + iu) ** ku
    with cr:
        seccion("Fórmulas")
        st.latex(r"P_{venc}=A\frac{1-(1+i)^{-n}}{i}\qquad F_{venc}=A\frac{(1+i)^n-1}{i}\qquad "
                 r"A=P\frac{i}{1-(1+i)^{-n}}=F\frac{i}{(1+i)^n-1}")
        st.latex(r"P_{antic}=P_{venc}(1+i)\qquad F_{antic}=F_{venc}(1+i)\qquad P_{dif}=\frac{P_{venc}}{(1+i)^k}")
        seccion("Resultados")
        res_u = pd.DataFrame({
            "Tipo de serie": ["Vencida", "Anticipada", f"Diferida {ku} periodos (vencida)"],
            "Cuota A": [cop(A), cop(A), cop(A)],
            "Valor presente": [cop(Pv), cop(Pa), cop(Pd)],
            "Valor futuro": [cop(Fv), cop(Fa), cop(Fv)],
            "Total aportado": [cop(A * nu)] * 3,
        })
        tabla(res_u)
    t0 = 0 if tipo_g == "Anticipada" else 1
    per = np.arange(0, nu + 1)
    flujo = np.array([A if (t0 <= k < t0 + nu) else 0 for k in per])
    acum = []
    s = 0.0
    for k in per:
        s = s * (1 + iu) + flujo[k]
        acum.append(s)
    c_a, c_b = st.columns(2)
    with c_a:
        fig = go.Figure()
        fig.add_bar(x=per, y=flujo, name="Cuota", marker_color=AZ_CLARO)
        fig.add_scatter(x=per, y=np.cumsum(flujo), name="Aportes sin intereses", line=dict(color=AZ_ACERO, dash="dot"),
                        yaxis="y2")
        estilo(fig, f"Flujo de pagos de la serie {tipo_g.lower()}", "Periodo", "Cuota (COP)")
        fig.update_layout(yaxis2=dict(overlaying="y", side="right", title="Acumulado (COP)", showgrid=False))
        graf(fig)
    with c_b:
        fig = go.Figure()
        fig.add_scatter(x=per, y=acum, fill="tozeroy", name="Saldo con intereses", line=dict(color=AZ_MEDIO, width=3),
                        fillcolor="rgba(30,90,168,0.18)")
        fig.add_scatter(x=per, y=np.cumsum(flujo), name="Sólo aportes", line=dict(color=AZ_MARINO, dash="dash"))
        estilo(fig, "Valor acumulado de la serie", "Periodo", "Valor (COP)")
        graf(fig)
    p_npf = npf.pv(iu, nu, -A)
    p_npf_a = npf.pv(iu, nu, -A, when="begin")
    verificacion(f"numpy_financial.pv vencida = {cop(p_npf, 2)} y anticipada = {cop(p_npf_a, 2)}; "
                 f"fórmulas: {cop(Pv, 2)} y {cop(Pa, 2)}. Saldo final del gráfico = {cop(acum[-1], 2)}.",
                 cerca(p_npf, Pv) and cerca(p_npf_a, Pa))

# =============================================================================
# MODULO 5: GRADIENTES
# =============================================================================
with TABS[5]:
    st.markdown("## Módulo de gradientes aritmético y geométrico")
    ce, cr = st.columns([1, 2])
    with ce:
        seccion("Parámetros de entrada")
        A1 = st.number_input("Primera cuota A1 (COP)", min_value=0, value=400_000, step=10_000, key="g_A1")
        G = st.number_input("Gradiente aritmético G (COP por periodo, puede ser negativo)", value=10_000,
                            step=1_000, key="g_G")
        gg = st.slider("Gradiente geométrico g (% por periodo)", -5.0, 10.0, 1.5, 0.1, key="g_g") / 100
        ig = st.slider("Tasa periódica i (%)", 0.05, 5.0, 1.0, 0.01, key="g_i") / 100
        ng = st.slider("Número de periodos n", 2, 240, 36, key="g_n")
    fa = ig * (1 + ig) ** ng / ((1 + ig) ** ng - 1)
    P_ar = vp_aritmetico(A1, G, ig, ng)
    F_ar = P_ar * (1 + ig) ** ng
    A_ar = P_ar * fa
    P_ge = vp_geometrico(A1, gg, ig, ng)
    F_ge = P_ge * (1 + ig) ** ng
    A_ge = P_ge * fa
    with cr:
        seccion("Fórmulas")
        st.latex(r"P_{arit}=A_1\frac{1-(1+i)^{-n}}{i}+\frac{G}{i}\left[\frac{1-(1+i)^{-n}}{i}-\frac{n}{(1+i)^n}\right]")
        st.latex(r"P_{geom}=A_1\frac{1-\left(\frac{1+g}{1+i}\right)^n}{i-g}\ (i\neq g)\qquad "
                 r"P_{geom}=\frac{nA_1}{1+i}\ (i=g)")
        st.latex(r"F=P(1+i)^n\qquad A_{eq}=P\frac{i(1+i)^n}{(1+i)^n-1}")
        seccion("Resultados")
        tabla(pd.DataFrame({
            "Gradiente": ["Aritmético", "Geométrico"],
            "Última cuota": [cop(A1 + (ng - 1) * G), cop(A1 * (1 + gg) ** (ng - 1))],
            "Valor presente": [cop(P_ar), cop(P_ge)],
            "Valor futuro": [cop(F_ar), cop(F_ge)],
            "Cuota uniforme equivalente": [cop(A_ar), cop(A_ge)],
        }))
    kk = np.arange(1, ng + 1)
    fl_ar = A1 + (kk - 1) * G
    fl_ge = A1 * (1 + gg) ** (kk - 1)
    c_a, c_b = st.columns(2)
    with c_a:
        fig = go.Figure()
        fig.add_bar(x=kk, y=fl_ar, name="Aritmético", marker_color=AZ_MEDIO)
        fig.add_bar(x=kk, y=fl_ge, name="Geométrico", marker_color=AZ_CIELO)
        fig.add_hline(y=A_ar, line_dash="dash", line_color=AZ_MARINO, annotation_text="Cuota equivalente aritm.")
        estilo(fig, "Flujo de cuotas de cada gradiente", "Periodo", "Cuota (COP)")
        fig.update_layout(barmode="group")
        graf(fig)
    with c_b:
        def acumular(fl):
            s, out = 0.0, [0.0]
            for v in fl:
                s = s * (1 + ig) + v
                out.append(s)
            return out
        fig = go.Figure()
        fig.add_scatter(x=np.arange(ng + 1), y=acumular(fl_ar), name="Aritmético", line=dict(color=AZ_MEDIO, width=3))
        fig.add_scatter(x=np.arange(ng + 1), y=acumular(fl_ge), name="Geométrico",
                        line=dict(color=AZ_CLARO, width=3, dash="dash"))
        estilo(fig, "Valor acumulado de cada gradiente", "Periodo", "Valor (COP)")
        graf(fig)
    vp_man_ar = float(np.sum(fl_ar / (1 + ig) ** kk))
    vp_man_ge = float(np.sum(fl_ge / (1 + ig) ** kk))
    npv_ar = npf.npv(ig, np.concatenate([[0], fl_ar]))
    verificacion(f"Suma descontada cuota a cuota: aritmético {cop(vp_man_ar, 2)} (npf.npv {cop(npv_ar, 2)}), "
                 f"geométrico {cop(vp_man_ge, 2)}; fórmulas: {cop(P_ar, 2)} y {cop(P_ge, 2)}.",
                 cerca(vp_man_ar, P_ar) and cerca(vp_man_ge, P_ge) and cerca(npv_ar, P_ar))

# =============================================================================
# MODULO 6: TABLAS DE AMORTIZACION
# =============================================================================
with TABS[6]:
    st.markdown("## Módulo de tablas de amortización")
    ce, cr = st.columns([1, 2])
    with ce:
        seccion("Parámetros del crédito")
        Pa_ = st.number_input("Capital (COP)", min_value=100_000, value=50_000_000, step=1_000_000, key="a_P")
        ta = st.slider("Tasa (%)", 0.5, 40.0, 14.0, 0.05, key="a_t") / 100
        tipo_ta = st.selectbox("Tipo de tasa", ["Efectiva anual", "Nominal anual (capitaliza con el pago)",
                                                "Periódica (del periodo de pago)"], key="a_tipo")
        plazo_a = st.slider("Plazo (años)", 1, 30, 5, key="a_plazo")
        per_a = st.selectbox("Periodicidad de pago", ["Mensual", "Trimestral", "Semestral", "Anual"], key="a_per")
        sistema = st.radio("Sistema de amortización", ["Cuota fija", "Abono constante a capital"], key="a_sis")
    m_a = PERIODICIDADES[per_a]
    if tipo_ta == "Efectiva anual":
        i_a = periodica_desde_ea(ta, m_a)
    elif tipo_ta.startswith("Nominal"):
        i_a = ta / m_a
    else:
        i_a = ta
    n_a = plazo_a * m_a
    t_fija = tabla_amortizacion(Pa_, i_a, n_a, "Cuota fija")
    t_abono = tabla_amortizacion(Pa_, i_a, n_a, "Abono constante a capital")
    t_sel = t_fija if sistema == "Cuota fija" else t_abono
    with cr:
        seccion("Fórmulas")
        st.latex(r"\text{Cuota fija: }A=P\frac{i}{1-(1+i)^{-n}}\qquad I_k=S_{k-1}\,i\qquad "
                 r"Ab_k=A-I_k\qquad S_k=S_{k-1}-Ab_k")
        st.latex(r"\text{Abono constante: }Ab=\frac{P}{n}\qquad C_k=Ab+S_{k-1}\,i")
        seccion("Totales y comparación entre sistemas")
        comp = pd.DataFrame({
            "Sistema": ["Cuota fija", "Abono constante a capital"],
            "Primera cuota": [cop(t_fija.Cuota[1]), cop(t_abono.Cuota[1])],
            "Última cuota": [cop(t_fija.Cuota.iloc[-1]), cop(t_abono.Cuota.iloc[-1])],
            "Intereses pagados": [cop(t_fija["Interés"].sum()), cop(t_abono["Interés"].sum())],
            "Total pagado": [cop(t_fija.Cuota.sum()), cop(t_abono.Cuota.sum())],
        })
        tabla(comp)
        fila_kpis([("Tasa periódica", pct(i_a, 4), f"E.A. {pct((1 + i_a) ** m_a - 1)}"),
                   ("Número de cuotas", str(n_a), per_a),
                   ("Ahorro en intereses con abono constante",
                    cop(t_fija["Interés"].sum() - t_abono["Interés"].sum()), "frente a cuota fija")])
    c_a, c_b = st.columns(2)
    with c_a:
        fig = go.Figure()
        fig.add_scatter(x=t_fija.Periodo, y=t_fija.Saldo, name="Cuota fija", fill="tozeroy",
                        line=dict(color=AZ_MEDIO), fillcolor="rgba(30,90,168,0.15)")
        fig.add_scatter(x=t_abono.Periodo, y=t_abono.Saldo, name="Abono constante",
                        line=dict(color=AZ_MARINO, dash="dash", width=2.5))
        estilo(fig, "Evolución del saldo por sistema", "Periodo", "Saldo (COP)")
        graf(fig)
    with c_b:
        d = t_sel.iloc[1:]
        fig = go.Figure()
        fig.add_bar(x=d.Periodo, y=d["Abono a capital"], name="Abono a capital", marker_color=AZ_MEDIO)
        fig.add_bar(x=d.Periodo, y=d["Interés"], name="Interés", marker_color=AZ_CIELO)
        estilo(fig, f"Composición de la cuota ({sistema.lower()})", "Periodo", "Valor (COP)")
        fig.update_layout(barmode="stack")
        graf(fig)
    seccion(f"Tabla de amortización completa ({sistema.lower()})")
    tabla(fmt_tabla_amort(t_sel))
    suma_ab = t_sel["Abono a capital"].sum()
    pmt = -npf.pmt(i_a, n_a, Pa_)
    verificacion(f"Suma de abonos a capital = {cop(suma_ab, 2)} = monto prestado {cop(Pa_, 2)}; "
                 f"saldo final = {cop(t_sel.Saldo.iloc[-1], 2)}; numpy_financial.pmt = {cop(pmt, 2)} "
                 f"vs cuota fija {cop(t_fija.Cuota[1], 2)}.",
                 cerca(suma_ab, Pa_) and abs(t_sel.Saldo.iloc[-1]) < 1 and cerca(pmt, t_fija.Cuota[1]))

# =============================================================================
# CASO 1: CREDITO DE VIVIENDA FNA vs BANCO CAJA SOCIAL
# =============================================================================
with TABS[7]:
    st.markdown("## Caso 1. Crédito de vivienda: Fondo Nacional del Ahorro vs Banco Caja Social")
    nota("Pregunta: ¿con cuál entidad sale más económico financiar la vivienda según el ingreso, el tipo de "
         "vivienda (VIS o No VIS), si es nueva o usada y si se compra sobre planos o ya edificada, incluyendo "
         "avalúo, estudio de títulos y escrituración?")
    e1, e2, e3 = st.columns(3)
    with e1:
        seccion("Vivienda")
        st.number_input("Valor de la vivienda (COP)", min_value=50_000_000, value=D["c1_valor"],
                        step=5_000_000, key="c1_valor")
        st.radio("Estado", ["Nueva", "Usada"], key="c1_estado", horizontal=True)
        if ss("c1_estado") == "Nueva":
            st.radio("Modalidad de compra", ["Sobre planos", "Edificada (entrega inmediata)"], key="c1_modalidad")
            st.checkbox("Proyecto financiado por Banco Caja Social (aplica descuento de tasa)", value=D["c1_proy_fin"],
                        key="c1_proy_fin")
        else:
            st.caption("Vivienda usada: se compra edificada y sin descuento de proyecto.")
        st.number_input("Tope VIS (SMMLV)", min_value=90, max_value=200, value=D["c1_tope_vis"], step=5,
                        key="c1_tope_vis")
    with e2:
        seccion("Solicitante")
        st.number_input("Ingreso mensual del hogar (COP)", min_value=500_000, value=D["c1_ingreso"],
                        step=250_000, key="c1_ingreso")
        st.selectbox("Vinculación al FNA", list(FNA_TASAS), key="c1_afiliacion")
        st.checkbox("Generación FNA (18 a 28 años): -0,5 p.p. y sin costo de avalúo ni estudio de títulos",
                    value=D["c1_joven"], key="c1_joven")
        st.slider("Plazo del crédito (años)", 5, 30, D["c1_plazo"], key="c1_plazo")
    with e3:
        seccion("Plan de ahorro para la cuota inicial")
        st.slider("Meses de ahorro (o meses hasta la entrega si es sobre planos)", 6, 60, D["c1_meses_plan"],
                  key="c1_meses_plan")
        st.slider("Tasa E.A. de la cuenta de ahorro (%)", 0.0, 15.0, D["c1_tasa_ahorro"], 0.05, key="c1_tasa_ahorro")
        st.slider("Crecimiento anual del aporte (gradiente, %)", 0.0, 15.0, D["c1_g_plan"], 0.5, key="c1_g_plan")
    with st.expander("Ajustar tasas, porcentajes de financiación y gastos de trámite (supuestos editables)"):
        a1, a2, a3 = st.columns(3)
        with a1:
            st.markdown("**Tasas**")
            st.number_input("Tasa E.A. manual FNA (%) — 0 usa la cartelera", 0.0, 30.0, D["c1_tasa_fna_manual"],
                            0.05, key="c1_tasa_fna_manual")
            st.number_input("Tasa E.A. manual Caja Social (%) — 0 usa el dato publicado", 0.0, 30.0,
                            D["c1_tasa_cs_manual"], 0.05, key="c1_tasa_cs_manual")
            st.number_input("Descuento Caja Social en proyectos financiados (p.p.)", 0.0, 3.0, D["c1_desc_cs"], 0.1,
                            key="c1_desc_cs")
        with a2:
            st.markdown("**Porcentaje de financiación (%)**")
            st.slider("FNA - VIS", 50, 100, D["c1_ltv_fna_vis"], key="c1_ltv_fna_vis")
            st.slider("FNA - No VIS", 50, 100, D["c1_ltv_fna_novis"], key="c1_ltv_fna_novis")
            st.slider("Caja Social - VIS", 50, 100, D["c1_ltv_cs_vis"], key="c1_ltv_cs_vis")
            st.slider("Caja Social - No VIS", 50, 100, D["c1_ltv_cs_novis"], key="c1_ltv_cs_novis")
        with a3:
            st.markdown("**Gastos de trámite**")
            st.number_input("Avalúo FNA (COP)", 0, 3_000_000, D["c1_aval_fna"], 10_000, key="c1_aval_fna")
            st.number_input("Estudio de títulos FNA (COP)", 0, 3_000_000, D["c1_tit_fna"], 10_000, key="c1_tit_fna")
            st.number_input("Avalúo Caja Social (COP)", 0, 3_000_000, D["c1_aval_cs"], 10_000, key="c1_aval_cs")
            st.number_input("Estudio de títulos Caja Social (COP)", 0, 3_000_000, D["c1_tit_cs"], 10_000,
                            key="c1_tit_cs")
            st.number_input("Derechos notariales comprador (% del valor)", 0.0, 2.0, D["c1_notaria"], 0.01,
                            key="c1_notaria")
            st.number_input("Impuesto de registro / beneficencia (%)", 0.0, 3.0, D["c1_benef"], 0.05, key="c1_benef")
            st.number_input("Derechos de registro (%)", 0.0, 2.0, D["c1_registro"], 0.05, key="c1_registro")

    r1 = calc_caso1(params_c1())
    E = r1["ent"]
    fna, cs = E["Fondo Nacional del Ahorro"], E["Banco Caja Social"]
    st.markdown(f"<div class='nota'>Clasificación: <b>{r1['tipo']}</b> (tope {cop(r1['tope'])}). "
                f"Rango salarial: <b>{r1['rango']}</b> ({num(ss('c1_ingreso') / SMMLV, 2)} SMMLV). "
                f"Compra: <b>{ss('c1_estado')}"
                f"{' - ' + ss('c1_modalidad') if ss('c1_estado') == 'Nueva' else ''}</b>.</div>",
                unsafe_allow_html=True)

    seccion("Fórmulas utilizadas")
    st.latex(r"i_{mv}=(1+EA)^{1/12}-1\qquad A=P\frac{i_{mv}}{1-(1+i_{mv})^{-n}}\qquad "
             r"\text{Intereses}=nA-P\qquad \frac{A}{\text{Ingreso}}\le 30\%")
    st.latex(r"\text{Plan uniforme: }A=CI\frac{i}{(1+i)^m-1}\qquad \text{Plan gradiente: }"
             r"A_1=CI\frac{i-g}{(1+i)^m-(1+g)^m}")

    seccion("Comparación de las dos ofertas")
    filas_cmp = [
        ("Tasa efectiva anual", pct(fna["tasa"]), pct(cs["tasa"])),
        ("Tasa nominal mes vencido equivalente", pct(fna["nominal_mv"]) + " NMV", pct(cs["nominal_mv"]) + " NMV"),
        ("Tasa mensual", pct(fna["im"], 4), pct(cs["im"], 4)),
        ("Porcentaje financiado", pct(fna["ltv"], 0), pct(cs["ltv"], 0)),
        ("Monto del préstamo", cop(fna["monto"]), cop(cs["monto"])),
        ("Cuota inicial", cop(fna["ci"]), cop(cs["ci"])),
        ("Cuota mensual", cop(fna["cuota"]), cop(cs["cuota"])),
        ("Cuota / ingreso", pct(fna["rel"], 1), pct(cs["rel"], 1)),
        ("Cumple capacidad de pago (30 %)", "Sí" if fna["cumple"] else "No", "Sí" if cs["cumple"] else "No"),
        ("Intereses totales", cop(fna["intereses"]), cop(cs["intereses"])),
        ("Avalúo", cop(fna["avaluo"]), cop(cs["avaluo"])),
        ("Estudio de títulos", cop(fna["titulos"]), cop(cs["titulos"])),
        ("Escrituración y registro", cop(fna["escrituracion"]), cop(cs["escrituracion"])),
        ("Valor total pagado", cop(fna["total"]), cop(cs["total"])),
        ("Costo de financiación (intereses + gastos)", cop(fna["costo_fin"]), cop(cs["costo_fin"])),
        ("Comparación justa: monto igual financiado", cop(fna["monto_c"]), cop(cs["monto_c"])),
        ("Cuota con monto igual", cop(fna["cuota_c"]), cop(cs["cuota_c"])),
        ("Intereses + gastos con monto igual", cop(fna["costo_c"]), cop(cs["costo_c"])),
    ]
    tabla(pd.DataFrame(filas_cmp, columns=["Concepto", "Fondo Nacional del Ahorro", "Banco Caja Social"]))
    otra = [k for k in E if k != r1["mejor"]][0]
    st.markdown(f"<div class='caso'><h4>Decisión recomendada</h4>Financiar con <b>{r1['mejor']}</b>. "
                f"Prestando el mismo monto ({cop(fna['monto_c'])}) sus intereses más gastos suman "
                f"{cop(E[r1['mejor']]['costo_c'])} frente a {cop(E[otra]['costo_c'])} de {otra}: una diferencia de "
                f"{cop(abs(fna['costo_c'] - cs['costo_c']))}. El FNA financia hasta {pct(fna['ltv'], 0)} y Caja Social "
                f"hasta {pct(cs['ltv'], 0)}, lo que cambia la cuota inicial que hay que reunir. "
                f"{'Ojo: ninguna cuota cabe en el 30 % del ingreso; conviene ampliar el plazo o la cuota inicial.' if not (fna['rel_c'] <= 0.3 or cs['rel_c'] <= 0.3) else ''}"
                f"</div>", unsafe_allow_html=True)

    c_a, c_b = st.columns(2)
    with c_a:
        conceptos = ["Cuota inicial", "Capital financiado", "Intereses", "Avalúo + títulos", "Escrituración"]
        fig = go.Figure()
        for nombre, e_, col in [("FNA", fna, AZ_MEDIO), ("Caja Social", cs, AZ_CLARO)]:
            fig.add_bar(x=conceptos, y=[e_["ci"], e_["monto"], e_["intereses"], e_["avaluo"] + e_["titulos"],
                                        e_["escrituracion"]], name=nombre, marker_color=col)
        fig.update_yaxes(type="log")
        estilo(fig, "Componentes del total pagado (escala logarítmica)", "", "COP")
        fig.update_layout(barmode="group")
        graf(fig)
    with c_b:
        fig = go.Figure()
        fig.add_scatter(x=fna["tabla"].Periodo, y=fna["tabla"].Saldo, name="Saldo FNA",
                        line=dict(color=AZ_MEDIO, width=3))
        fig.add_scatter(x=cs["tabla"].Periodo, y=cs["tabla"].Saldo, name="Saldo Caja Social",
                        line=dict(color=AZ_MARINO, width=3, dash="dash"))
        fig.add_scatter(x=fna["tabla"].Periodo, y=fna["tabla"]["Interés"].cumsum(), name="Intereses acumulados FNA",
                        line=dict(color=AZ_CLARO, dash="dot"))
        fig.add_scatter(x=cs["tabla"].Periodo, y=cs["tabla"]["Interés"].cumsum(),
                        name="Intereses acumulados Caja Social", line=dict(color=AZ_ACERO, dash="dot"))
        estilo(fig, "Saldo del crédito e intereses acumulados", "Mes", "COP")
        graf(fig)

    seccion("Comparación por rango salarial y tipo de vivienda")
    sal = [1.5, 3.0, 5.0, 8.0]
    filas_h, z, ytxt = [], [], []
    for nombre, f_ in [("FNA Cesantías", lambda r, t: FNA_TASAS["Cesantías"][r]),
                       ("FNA AVC", lambda r, t: FNA_TASAS["Ahorro Voluntario Contractual (AVC)"][r]),
                       ("Caja Social VIS sobre planos (proy. financiado)", lambda r, t: CAJA_TASAS["VIS"] - ss("c1_desc_cs") / 100),
                       ("Caja Social VIS edificada / usada", lambda r, t: CAJA_TASAS["VIS"]),
                       ("Caja Social No VIS sobre planos (proy. financiado)", lambda r, t: CAJA_TASAS["No VIS"] - ss("c1_desc_cs") / 100),
                       ("Caja Social No VIS edificada / usada", lambda r, t: CAJA_TASAS["No VIS"])]:
        z.append([f_(rango_idx(s_ * SMMLV), None) * 100 for s_ in sal])
        ytxt.append(nombre)
    c_a, c_b = st.columns(2)
    with c_a:
        fig = go.Figure(go.Heatmap(z=z, x=[f"{num(s_, 1)} SMMLV" for s_ in sal], y=ytxt, colorscale=ESCALA_AZUL,
                                   text=[[pct(v / 100) for v in row] for row in z], texttemplate="%{text}",
                                   colorbar=dict(title="E.A. %")))
        estilo(fig, "Tasa E.A. por ingreso y modalidad", "Ingreso del hogar", "", h=420, leyenda=False)
        graf(fig)
    with c_b:
        n_ = r1["n"]
        fig = go.Figure()
        for nombre, color, tfun in [
            ("FNA (vinculación elegida)", AZ_MEDIO,
             lambda s_: FNA_TASAS[ss("c1_afiliacion")][rango_idx(s_ * SMMLV)] - (0.005 if ss("c1_joven") else 0)),
            ("Banco Caja Social", AZ_MARINO, lambda s_: cs["tasa"])]:
            monto_ = fna["monto"] if "FNA" in nombre else cs["monto"]
            rel = [cuota_fija(monto_, periodica_desde_ea(tfun(s_), 12), n_) / (s_ * SMMLV) * 100 for s_ in sal]
            fig.add_bar(x=[f"{num(s_, 1)} SMMLV" for s_ in sal], y=rel, name=nombre, marker_color=color,
                        text=[f"{num(v, 1)} %" for v in rel], textposition="outside")
        fig.add_hline(y=30, line_dash="dash", line_color=AZ_MARINO, annotation_text="Tope 30 %")
        estilo(fig, "Cuota como porcentaje del ingreso, por rango salarial", "Ingreso del hogar", "Cuota / ingreso (%)",
               h=420)
        fig.update_layout(barmode="group")
        graf(fig)

    seccion("Comparación de créditos con distintos plazos")
    plazos = [5, 10, 15, 20, 25, 30]
    fig = go.Figure()
    for nombre, e_, col in [("FNA", fna, AZ_MEDIO), ("Caja Social", cs, AZ_MARINO)]:
        tot = [cuota_fija(e_["monto"], e_["im"], y * 12) * y * 12 - e_["monto"] for y in plazos]
        cuo = [cuota_fija(e_["monto"], e_["im"], y * 12) for y in plazos]
        fig.add_bar(x=plazos, y=tot, name=f"Intereses totales {nombre}", marker_color=col, opacity=0.85)
        fig.add_scatter(x=plazos, y=cuo, name=f"Cuota mensual {nombre}", yaxis="y2", mode="lines+markers",
                        line=dict(color=AZ_CLARO if nombre == "FNA" else AZ_ACERO, width=3))
    estilo(fig, "Intereses totales (barras) y cuota mensual (líneas) según el plazo", "Plazo (años)",
           "Intereses totales (COP)", h=420)
    fig.update_layout(barmode="group", yaxis2=dict(overlaying="y", side="right", title="Cuota mensual (COP)",
                                                   showgrid=False))
    graf(fig)

    seccion("Plan de ahorro para reunir la cuota inicial")
    ent_plan = st.radio("Cuota inicial de la entidad", ["Fondo Nacional del Ahorro", "Banco Caja Social"],
                        horizontal=True, key="c1_ent_plan")
    ep = E[ent_plan]
    mp, ia, gm = r1["mp"], r1["i_aho"], r1["g_m"]
    etiqueta = "pagos a la constructora durante la obra" if r1["sobre_planos"] else "ahorro previo a la compra"
    fila_kpis([("Cuota inicial a reunir", cop(ep["ci"]), etiqueta),
               ("Aporte mensual uniforme", cop(ep["a_unif"]), f"{mp} meses"),
               ("Primer aporte con gradiente", cop(ep["a1_grad"]), f"crece {pct(ss('c1_g_plan') / 100, 1)} anual"),
               ("Último aporte con gradiente", cop(ep["a1_grad"] * (1 + gm) ** (mp - 1)), "")])
    mm = np.arange(1, mp + 1)
    au = np.full(mp, ep["a_unif"])
    ag = ep["a1_grad"] * (1 + gm) ** (mm - 1)
    s_u, s_g = [0.0], [0.0]
    for k_ in range(mp):
        s_u.append(s_u[-1] * (1 + ia) + au[k_])
        s_g.append(s_g[-1] * (1 + ia) + ag[k_])
    c_a, c_b = st.columns(2)
    with c_a:
        fig = go.Figure()
        fig.add_bar(x=mm, y=au, name="Uniforme", marker_color=AZ_CIELO)
        fig.add_bar(x=mm, y=ag, name="Gradiente geométrico", marker_color=AZ_MEDIO)
        estilo(fig, "Aportes mensuales del plan", "Mes", "Aporte (COP)")
        fig.update_layout(barmode="group")
        graf(fig)
    with c_b:
        fig = go.Figure()
        fig.add_scatter(x=np.arange(mp + 1), y=s_u, name="Saldo plan uniforme", fill="tozeroy",
                        line=dict(color=AZ_CLARO), fillcolor="rgba(93,173,226,0.18)")
        fig.add_scatter(x=np.arange(mp + 1), y=s_g, name="Saldo plan gradiente", line=dict(color=AZ_MARINO, width=3))
        fig.add_hline(y=ep["ci"], line_dash="dash", line_color=AZ_MARINO, annotation_text="Meta: cuota inicial")
        estilo(fig, "Saldo acumulado hacia la cuota inicial", "Mes", "Saldo (COP)")
        graf(fig)

    seccion("Tabla de amortización de la entidad recomendada")
    tabla(fmt_tabla_amort(E[r1["mejor"]]["tabla"]))
    tm = E[r1["mejor"]]["tabla"]
    verificacion(f"Suma de abonos = {cop(tm['Abono a capital'].sum(), 2)} igual al préstamo "
                 f"{cop(E[r1['mejor']]['monto'], 2)}; saldo final {cop(tm.Saldo.iloc[-1], 2)}; "
                 f"plan uniforme alcanza {cop(s_u[-1], 2)} y plan gradiente {cop(s_g[-1], 2)} "
                 f"(meta {cop(ep['ci'], 2)}).",
                 cerca(tm["Abono a capital"].sum(), E[r1["mejor"]]["monto"]) and abs(tm.Saldo.iloc[-1]) < 1
                 and (ep["ci"] == 0 or (cerca(s_u[-1], ep["ci"]) and cerca(s_g[-1], ep["ci"]))))

# =============================================================================
# CASO 2: CDT vs CUENTA DE AHORROS (BANCOLOMBIA y NU)
# =============================================================================
with TABS[8]:
    st.markdown("## Caso 2. ¿CDT o cuenta de ahorros? Bancolombia vs Nu")
    nota("Pregunta central: ¿es más rentable invertir una cantidad de dinero en un CDT o mantenerla en una "
         "cuenta de ahorros durante el mismo periodo?")
    e1, e2, e3 = st.columns(3)
    with e1:
        seccion("Inversión")
        st.number_input("Monto a invertir (COP)", min_value=50_000, value=D["c2_monto"], step=500_000, key="c2_monto")
        st.select_slider("Plazo (días)", options=list(NU_CDT), value=D["c2_dias"], key="c2_dias")
        usar_tabla = st.checkbox("Usar la tasa del CDT Nu publicada para el plazo elegido", value=True,
                                 key="c2_usar_tabla")
    with e2:
        seccion("Tasas E.A. anunciadas (%)")
        if usar_tabla:
            st.session_state["c2_tasa_nu_cdt"] = NU_CDT[int(ss("c2_dias"))] * 100
        st.number_input("CDT Nu", 0.0, 25.0, step=0.05, key="c2_tasa_nu_cdt", disabled=usar_tabla)
        st.number_input("CDT Bancolombia", 0.0, 25.0, D["c2_tasa_bc_cdt"], 0.05, key="c2_tasa_bc_cdt")
        st.number_input("Cuenta Nu (Cajitas)", 0.0, 25.0, D["c2_tasa_nu_aho"], 0.05, key="c2_tasa_nu_aho")
        st.number_input("Cuenta de ahorros Bancolombia", 0.0, 25.0, D["c2_tasa_bc_aho"], 0.01, key="c2_tasa_bc_aho")
    with e3:
        seccion("Retención en la fuente")
        st.slider("Retención CDT (% de los rendimientos)", 0.0, 15.0, D["c2_ret_cdt"], 0.5, key="c2_ret_cdt")
        st.slider("Retención cuentas de ahorro (%)", 0.0, 15.0, D["c2_ret_aho"], 0.5, key="c2_ret_aho")
        st.number_input("Umbral diario de retención en ahorros (UVT)", 0.0, 1.0, D["c2_umbral_uvt"], 0.005,
                        format="%.3f", key="c2_umbral_uvt")
    r2 = calc_caso2(params_c2())
    R = r2["res"]
    seccion("Fórmulas")
    st.latex(r"\text{CDT: }F=P(1+EA)^{d/365}\qquad \text{Ahorros: }i_d=(1+EA)^{1/365}-1,\ "
             r"S_t=S_{t-1}\left(1+i_d(1-r\cdot\mathbb{1}[S_{t-1}i_d>0{,}055\,UVT])\right)")
    st.latex(r"\text{Interés neto}=\text{Interés bruto}(1-r)\qquad EA_{neta}=\left(\frac{F_{neto}}{P}\right)^{365/d}-1"
             r"\qquad \text{Simple: }F=P(1+i_m\,\tfrac{d}{30})")
    filas = []
    for k_, v in R.items():
        filas.append({"Alternativa": k_, "Tipo": v["tipo"], "E.A. anunciada": pct(v["ea"]),
                      "Tasa diaria equivalente": pct(periodica_desde_ea(v["ea"], 365), 5),
                      "Tasa N.M.V. equivalente": pct(periodica_desde_ea(v["ea"], 12) * 12),
                      "Rendimiento bruto": cop(v["bruto"]), "Retención": cop(v["ret"]),
                      "Rendimiento neto": cop(v["neto"]), "Total recibido": cop(v["final"]),
                      "E.A. neta": pct(v["ea_neta"])})
    seccion("Equivalencia de tasas y resultados al final del plazo")
    tabla(pd.DataFrame(filas))
    mej = R[r2["mejor"]]
    st.markdown(f"<div class='caso'><h4>Decisión recomendada</h4>Con {cop(ss('c2_monto'))} a "
                f"{int(ss('c2_dias'))} días conviene <b>{r2['mejor']}</b>: recibe {cop(mej['final'])} con una "
                f"E.A. neta de {pct(mej['ea_neta'])}. Frente a la cuenta de ahorros Bancolombia gana "
                f"{cop(mej['final'] - R['Cuenta de ahorros Bancolombia']['final'])} adicionales. "
                f"La Cajita Nu ofrece liquidez diaria, pero su tasa puede cambiar; el CDT fija la tasa hasta el "
                f"vencimiento.</div>", unsafe_allow_html=True)
    c_a, c_b = st.columns(2)
    dias_ = int(ss("c2_dias"))
    with c_a:
        fig = go.Figure()
        for (k_, v), dash in zip(R.items(), ["solid", "dash", "dot", "dashdot"]):
            fig.add_scatter(x=np.arange(len(v["tray"])), y=v["tray"], name=k_, line=dict(dash=dash, width=2.5))
        estilo(fig, "Crecimiento del capital día a día (interés compuesto)", "Día", "Saldo (COP)")
        graf(fig)
    with c_b:
        nombres = list(R)
        cortos = {"CDT Nu": "CDT Nu", "CDT Bancolombia": "CDT Bancolombia", "Cuenta Nu (Cajitas)": "Cajitas Nu",
                  "Cuenta de ahorros Bancolombia": "Ahorros Bancolombia"}
        fig = go.Figure()
        fig.add_bar(x=[cortos[n_] for n_ in nombres], y=[R[n_]["neto"] for n_ in nombres], name="Rendimiento neto", marker_color=AZ_MEDIO)
        fig.add_bar(x=[cortos[n_] for n_ in nombres], y=[R[n_]["ret"] for n_ in nombres], name="Retención", marker_color=AZ_CIELO)
        estilo(fig, "Rendimiento neto y retención en la fuente", "", "COP")
        fig.update_layout(barmode="stack")
        graf(fig)
    c_a, c_b = st.columns(2)
    with c_a:
        ea_nu = ss("c2_tasa_nu_cdt") / 100
        i_m = periodica_desde_ea(ea_nu, 12)
        tt = np.arange(0, dias_ + 1, 30)
        fig = go.Figure()
        fig.add_scatter(x=tt, y=ss("c2_monto") * (1 + ea_nu) ** (tt / 365), name="Compuesto (CDT al vencimiento)",
                        line=dict(color=AZ_MEDIO, width=3))
        fig.add_scatter(x=tt, y=ss("c2_monto") * (1 + i_m * tt / 30), name="Simple (CDT con pago mensual sin reinvertir)",
                        line=dict(color=AZ_ACERO, width=3, dash="dash"))
        estilo(fig, "CDT Nu: interés simple vs compuesto", "Día", "Valor (COP)")
        graf(fig)
    with c_b:
        x_ = [f"{d_} d" for d_ in NU_CDT]
        fig = go.Figure()
        fig.add_scatter(x=x_, y=[v * 100 for v in NU_CDT.values()], mode="lines+markers+text", name="CDT Nu bruta",
                        text=[pct(v) for v in NU_CDT.values()], textposition="top center",
                        line=dict(color=AZ_MEDIO, width=3))
        fig.add_scatter(x=x_, y=[((1 + (((1 + v) ** (d_ / 365) - 1) * (1 - ss("c2_ret_cdt") / 100))) ** (365 / d_) - 1) * 100
                                 for d_, v in NU_CDT.items()], mode="lines+markers", name="CDT Nu neta",
                        line=dict(color=AZ_MARINO, dash="dash"))
        fig.add_hline(y=ss("c2_tasa_nu_aho"), line_dash="dot", line_color=AZ_CLARO, annotation_text="Cajitas Nu", annotation_position="bottom left")
        fig.add_hline(y=ss("c2_tasa_bc_cdt"), line_dash="dot", line_color=AZ_ACERO,
                      annotation_text="CDT Bancolombia 360 d", annotation_position="top left")
        estilo(fig, "Curva de tasas del CDT Nu por plazo (E.A.)", "Plazo", "Tasa E.A. (%)")
        graf(fig)

    seccion("Plan de ahorro con aportes periódicos: serie uniforme vs gradiente")
    p1, p2, p3_ = st.columns(3)
    p1.number_input("Aporte mensual inicial (COP)", min_value=0, value=D["c2_aporte"], step=50_000, key="c2_aporte")
    p2.slider("Incremento anual de la cuota (%)", 0.0, 20.0, D["c2_g"], 0.5, key="c2_g")
    p3_.slider("Duración del plan (meses)", 6, 120, D["c2_meses"], key="c2_meses")
    r2 = calc_caso2(params_c2())
    st.latex(r"F_{unif}=A\frac{(1+i)^n-1}{i}\qquad g_m=(1+g_a)^{1/12}-1\qquad "
             r"F_{grad}=A_1\frac{(1+i)^n-(1+g_m)^n}{i-g_m}")
    pl = r2["plan"]
    nplan = r2["n"]
    fila_kpis([("Nu - plan uniforme", cop(pl["Cuenta Nu (Cajitas)"]["uni"][-1]),
                f"aportado {cop(pl['Cuenta Nu (Cajitas)']['ap_u'][-1])}"),
               ("Nu - plan gradiente", cop(pl["Cuenta Nu (Cajitas)"]["gra"][-1]),
                f"aportado {cop(pl['Cuenta Nu (Cajitas)']['ap_g'][-1])}"),
               ("Bancolombia - plan uniforme", cop(pl["Cuenta de ahorros Bancolombia"]["uni"][-1]), ""),
               ("Bancolombia - plan gradiente", cop(pl["Cuenta de ahorros Bancolombia"]["gra"][-1]), "")])
    c_a, c_b = st.columns(2)
    with c_a:
        fig = go.Figure()
        xm = np.arange(nplan + 1)
        fig.add_scatter(x=xm, y=pl["Cuenta Nu (Cajitas)"]["gra"], name="Nu gradiente", fill="tozeroy",
                        line=dict(color=AZ_MEDIO), fillcolor="rgba(30,90,168,0.15)")
        fig.add_scatter(x=xm, y=pl["Cuenta Nu (Cajitas)"]["uni"], name="Nu uniforme", line=dict(color=AZ_CLARO, width=3))
        fig.add_scatter(x=xm, y=pl["Cuenta de ahorros Bancolombia"]["gra"], name="Bancolombia gradiente",
                        line=dict(color=AZ_MARINO, dash="dash"))
        fig.add_scatter(x=xm, y=pl["Cuenta de ahorros Bancolombia"]["uni"], name="Bancolombia uniforme",
                        line=dict(color=AZ_ACERO, dash="dot"))
        estilo(fig, "Saldo acumulado del plan de ahorro", "Mes", "Saldo (COP)")
        graf(fig)
    with c_b:
        nu_g = pl["Cuenta Nu (Cajitas)"]
        fig = go.Figure(go.Pie(labels=["Aportes", "Intereses ganados"],
                               values=[nu_g["ap_g"][-1], nu_g["gra"][-1] - nu_g["ap_g"][-1]], hole=0.5,
                               marker=dict(colors=[AZ_MEDIO, AZ_CIELO])))
        estilo(fig, "Composición del saldo final (Nu, plan gradiente)")
        graf(fig)
    i_nu = pl["Cuenta Nu (Cajitas)"]["i_m"]
    f_cerr = vf_serie(ss("c2_aporte"), i_nu, nplan)
    f_npf = npf.fv(i_nu, nplan, -ss("c2_aporte"), 0)
    gm2 = r2["g_m"]
    f_grad = ss("c2_aporte") * ((1 + i_nu) ** nplan - (1 + gm2) ** nplan) / (i_nu - gm2) if abs(i_nu - gm2) > 1e-12 \
        else ss("c2_aporte") * nplan * (1 + i_nu) ** (nplan - 1)
    verificacion(f"Plan uniforme Nu: fórmula {cop(f_cerr, 2)}, numpy_financial.fv {cop(f_npf, 2)}, simulación mes a mes "
                 f"{cop(pl['Cuenta Nu (Cajitas)']['uni'][-1], 2)}. Gradiente: fórmula {cop(f_grad, 2)} vs simulación "
                 f"{cop(pl['Cuenta Nu (Cajitas)']['gra'][-1], 2)}.",
                 cerca(f_cerr, f_npf) and cerca(f_cerr, pl["Cuenta Nu (Cajitas)"]["uni"][-1])
                 and cerca(f_grad, pl["Cuenta Nu (Cajitas)"]["gra"][-1]))

# =============================================================================
# CASO 3: INVERSION EN EL ETF VOO DESDE COLOMBIA
# =============================================================================
with TABS[9]:
    st.markdown("## Caso 3. Inversión en el ETF Vanguard S&P 500 (VOO) desde Colombia")
    nota("Se convierte el capital de pesos a dólares, se proyecta el crecimiento del ETF, se descuentan costos "
         "(diferencial cambiario, comisiones, gastos del fondo, retención sobre dividendos) y se regresa a pesos con "
         "la tasa de cambio proyectada.")
    e1, e2, e3 = st.columns(3)
    with e1:
        seccion("Inversión")
        st.number_input("Monto inicial (COP)", min_value=100_000, value=D["c3_inv"], step=500_000, key="c3_inv")
        st.slider("Horizonte (años)", 1, 30, D["c3_anios"], key="c3_anios")
        st.number_input("Aporte mensual adicional (COP, 0 = sin aportes)", min_value=0, value=D["c3_aporte"],
                        step=100_000, key="c3_aporte")
        st.slider("Crecimiento anual del aporte (gradiente, %)", 0.0, 15.0, D["c3_g_aporte"], 0.5, key="c3_g_aporte")
    with e2:
        seccion("Mercado")
        st.number_input("TRM inicial (COP por USD)", 1000.0, 8000.0, D["c3_trm"], 10.0, key="c3_trm")
        st.slider("Rentabilidad anual esperada de VOO en USD (%)", -10.0, 25.0, D["c3_r"], 0.25, key="c3_r")
        st.slider("Devaluación anual esperada del peso (%)", -10.0, 15.0, D["c3_dev"], 0.25, key="c3_dev")
        st.slider("Rendimiento por dividendos (%)", 0.0, 3.0, D["c3_div"], 0.01, key="c3_div")
    with e3:
        seccion("Costos")
        st.number_input("Gasto anual del fondo (expense ratio, %)", 0.0, 1.0, D["c3_er"], 0.01, key="c3_er")
        st.slider("Diferencial cambiario al comprar USD (%)", 0.0, 5.0, D["c3_spread_c"], 0.1, key="c3_spread_c")
        st.slider("Diferencial cambiario al vender USD (%)", 0.0, 5.0, D["c3_spread_v"], 0.1, key="c3_spread_v")
        st.number_input("Comisión del bróker por operación (USD)", 0.0, 50.0, D["c3_comision"], 0.5, key="c3_comision")
        st.slider("Retención de EE. UU. sobre dividendos (%)", 0.0, 40.0, D["c3_ret_div"], 1.0, key="c3_ret_div")
    p3 = params_c3()
    r3 = simular_voo(p3)
    seccion("Fórmulas")
    st.latex(r"USD_0=\frac{COP_0(1-s_c)}{TRM_0}\qquad TRM_t=TRM_0(1+dev)^{t/12}\qquad "
             r"i_m=(1+r)^{1/12}-1")
    st.latex(r"USD_t=USD_{t-1}(1+i_m)\left(1+\tfrac{div(1-ret)}{12}-\tfrac{ER}{12}\right)+\frac{A_t(1-s_c)}{TRM_t}"
             r"\qquad COP_n=USD_n\,TRM_n(1-s_v)")
    st.latex(r"\text{Tasa combinada: }(1+r)(1+dev)-1\qquad EA_{neta}=(1+TIR_{mensual})^{12}-1\qquad "
             r"A_t=A_1(1+g_m)^{t-1}")
    fila_kpis([("Valor futuro en COP", cop(r3["final_cop"]), f"{usd(r3['final_usd'])} a TRM {cop(r3['trm_n'], 2)}"),
               ("Total aportado", cop(r3["total_aportado"]), f"ganancia {cop(r3['ganancia'])}"),
               ("E.A. neta en pesos", pct(r3["ea_neta"]), f"tasa combinada bruta {pct(r3['combinada'])}"),
               ("Costos totales", cop(r3["costos"]), "cambio, comisiones (sin expense ratio)")])

    seccion("Escenarios de rentabilidad")
    with st.expander("Editar escenarios"):
        s1, s2, s3 = st.columns(3)
        esc_def = {"Pesimista": (4.0, -3.0), "Base": (10.0, 3.0), "Optimista": (13.36, 6.0)}
        esc = {}
        for col, (nom, (rr, dd)) in zip([s1, s2, s3], esc_def.items()):
            with col:
                st.markdown(f"**{nom}**")
                rr_ = st.number_input(f"Rentabilidad USD {nom} (%)", -20.0, 30.0, rr, 0.25, key=f"c3_esc_r_{nom}")
                dd_ = st.number_input(f"Devaluación {nom} (%)", -15.0, 20.0, dd, 0.25, key=f"c3_esc_d_{nom}")
                esc[nom] = (rr_, dd_)
    res_esc = {nom: simular_voo(p3, r=rr / 100, dev=dd / 100) for nom, (rr, dd) in esc.items()}
    tabla(pd.DataFrame([{"Escenario": nom, "Rent. USD": pct(esc[nom][0] / 100), "Devaluación": pct(esc[nom][1] / 100),
                         "Valor futuro COP": cop(v["final_cop"]), "Ganancia": cop(v["ganancia"]),
                         "E.A. neta COP": pct(v["ea_neta"])} for nom, v in res_esc.items()]))
    c_a, c_b = st.columns(2)
    meses_ = np.arange(r3["n"] + 1)
    with c_a:
        fig = go.Figure()
        cols_esc = {"Pesimista": AZ_ACERO, "Base": AZ_MEDIO, "Optimista": AZ_MARINO}
        for nom, v in res_esc.items():
            fig.add_scatter(x=meses_ / 12, y=v["tray_cop"], name=nom, line=dict(color=cols_esc[nom], width=3))
        fig.add_scatter(x=meses_ / 12, y=r3["aport"], name="Capital aportado", line=dict(color=AZ_CIELO, dash="dot"))
        estilo(fig, "Valor de la inversión en pesos por escenario", "Años", "Valor (COP)")
        graf(fig)
    with c_b:
        fig = go.Figure()
        fig.add_scatter(x=meses_ / 12, y=r3["tray_usd"], name="Valor en USD", line=dict(color=AZ_MEDIO, width=3))
        fig.add_scatter(x=meses_ / 12, y=r3["trm"], name="TRM proyectada", yaxis="y2",
                        line=dict(color=AZ_ACERO, dash="dash"))
        estilo(fig, "Escenario seleccionado: valor en dólares y tasa de cambio", "Años", "Valor (USD)")
        fig.update_layout(yaxis2=dict(overlaying="y", side="right", title="TRM (COP/USD)", showgrid=False))
        graf(fig)

    seccion("Variables que más afectan el resultado")
    c_a, c_b = st.columns(2)
    with c_a:
        base_ea = r3["ea_neta"]
        pruebas = [
            ("Rentabilidad USD ±4 p.p.", dict(r=(p3["r"] - 4) / 100), dict(r=(p3["r"] + 4) / 100)),
            ("Devaluación ±4 p.p.", dict(dev=(p3["dev"] - 4) / 100), dict(dev=(p3["dev"] + 4) / 100)),
            ("Diferencial cambiario ±1 p.p.", dict(spread_c=(p3["spread_c"] + 1) / 100),
             dict(spread_c=max(p3["spread_c"] - 1, 0) / 100)),
            ("Dividendos ±0,5 p.p.", dict(div=max(p3["div"] - 0.5, 0) / 100), dict(div=(p3["div"] + 0.5) / 100)),
            ("Expense ratio ±0,5 p.p.", dict(er=(p3["er"] + 0.5) / 100), dict(er=max(p3["er"] - 0.5, 0) / 100)),
        ]
        rows_t = []
        for nom, lo, hi in pruebas:
            a_ = simular_voo(p3, **lo)["ea_neta"]
            b_ = simular_voo(p3, **hi)["ea_neta"]
            rows_t.append((nom, min(a_, b_) - base_ea, max(a_, b_) - base_ea))
        rows_t.sort(key=lambda x: x[2] - x[1])
        fig = go.Figure()
        fig.add_bar(y=[x[0] for x in rows_t], x=[x[1] * 100 for x in rows_t], orientation="h", name="Variación a la baja",
                    marker_color=AZ_ACERO)
        fig.add_bar(y=[x[0] for x in rows_t], x=[x[2] * 100 for x in rows_t], orientation="h", name="Variación al alza",
                    marker_color=AZ_MEDIO)
        estilo(fig, f"Diagrama de tornado sobre la E.A. neta (base {pct(base_ea)})", "Cambio en la E.A. neta (p.p.)", "")
        fig.update_layout(barmode="relative")
        graf(fig)
    with c_b:
        rs = np.arange(-4, 18, 2)
        ds = np.arange(-8, 12, 2)
        zz = [[simular_voo(p3, r=r_ / 100, dev=d_ / 100)["ea_neta"] * 100 for r_ in rs] for d_ in ds]
        fig = go.Figure(go.Heatmap(z=zz, x=[f"{r_} %" for r_ in rs], y=[f"{d_} %" for d_ in ds], colorscale=ESCALA_AZUL,
                                   colorbar=dict(title="E.A. %"),
                                   hovertemplate="Rent. USD %{x}<br>Devaluación %{y}<br>E.A. neta %{z:.2f} %<extra></extra>"))
        estilo(fig, "E.A. neta en pesos según rentabilidad USD y devaluación", "Rentabilidad anual en USD",
               "Devaluación anual del peso", leyenda=False)
        graf(fig)

    seccion("Estrategias de aportes periódicos")
    total_inv = p3["inv"]
    n_m = int(p3["anios"] * 12)
    ap_unif = total_inv / n_m
    estr = {
        "Todo al inicio": simular_voo({**p3, "aporte": 0}),
        "Aporte inicial + aporte mensual elegido": simular_voo(p3),
        "Mismo capital repartido en cuotas mensuales iguales": simular_voo(
            {**p3, "inv": ap_unif, "aporte": ap_unif, "g_aporte": 0.0}),
    }
    c_a, c_b = st.columns(2)
    with c_a:
        fig = go.Figure()
        nombres_e = list(estr)
        fig.add_bar(x=nombres_e, y=[v["total_aportado"] for v in estr.values()], name="Total aportado",
                    marker_color=AZ_CIELO)
        fig.add_bar(x=nombres_e, y=[v["final_cop"] for v in estr.values()], name="Valor futuro", marker_color=AZ_MEDIO,
                    text=[pct(v["ea_neta"]) for v in estr.values()], textposition="outside")
        estilo(fig, "Valor futuro por estrategia (etiqueta: E.A. neta)", "", "COP")
        fig.update_layout(barmode="group")
        graf(fig)
    with c_b:
        hist = {"1 año": 22.28, "3 años": 20.58, "5 años": 13.36, "10 años": 15.47, "Desde 2010": 15.03}
        fig = go.Figure(go.Bar(x=list(hist), y=list(hist.values()), marker_color=PALETA[:5],
                               text=[f"{num(v, 2)} %" for v in hist.values()], textposition="outside"))
        fig.add_hline(y=p3["r"], line_dash="dash", line_color=AZ_MARINO, annotation_text="Supuesto actual")
        estilo(fig, "Rentabilidad histórica anualizada de VOO en USD (NAV, a 30-jun-2026)", "Periodo", "% anual",
               leyenda=False)
        graf(fig)
    c2_ = calc_caso2(params_c2())
    cdt_neta = c2_["res"]["CDT Nu"]["ea_neta"]
    gana = r3["ea_neta"] > cdt_neta
    st.markdown(f"<div class='caso'><h4>Decisión recomendada</h4>"
                f"{'Invertir en VOO' if gana else 'Preferir el CDT'}: con los supuestos actuales la E.A. neta en pesos "
                f"es {pct(r3['ea_neta'])} frente a {pct(cdt_neta)} del CDT Nu neto. "
                f"El resultado depende sobre todo de la rentabilidad del ETF en dólares y de la tasa de cambio "
                f"(ver tornado); en el escenario pesimista la E.A. neta sería {pct(res_esc['Pesimista']['ea_neta'])}. "
                f"VOO es adecuado para horizontes de 5 años o más y perfiles que toleran pérdidas temporales; "
                f"los costos de cambio pesan más en montos pequeños y plazos cortos.</div>", unsafe_allow_html=True)
    # verificacion con calculo cerrado (sin aportes, sin dividendos, sin costos)
    pv_ = {**p3, "aporte": 0, "div": 0.0, "er": 0.0, "spread_c": 0.0, "spread_v": 0.0, "comision": 0.0}
    sim = simular_voo(pv_)
    cerrado = p3["inv"] * ((1 + p3["r"] / 100) * (1 + p3["dev"] / 100)) ** p3["anios"]
    verificacion(f"Sin costos ni aportes la simulación da {cop(sim['final_cop'], 2)} y la fórmula cerrada "
                 f"P[(1+r)(1+dev)]^n = {cop(cerrado, 2)}; la TIR anual coincide con la tasa combinada "
                 f"({pct(sim['ea_neta'], 4)} vs {pct((1 + p3['r'] / 100) * (1 + p3['dev'] / 100) - 1, 4)}).",
                 cerca(sim["final_cop"], cerrado, 1e-6) and cerca(sim["ea_neta"],
                                                                   (1 + p3["r"] / 100) * (1 + p3["dev"] / 100) - 1, 1e-6))

# =============================================================================
# SUPUESTOS Y FUENTES
# =============================================================================
with TABS[10]:
    st.markdown("## Supuestos, convenciones y fuentes")
    seccion("Convenciones")
    tabla(pd.DataFrame([
        ("Interés simple", "Año comercial de 360 días o real de 365 días, a elección del usuario."),
        ("CDT y cuentas de ahorro", "Año de 365 días; el CDT liquida al vencimiento con F = P(1+EA)^(d/365); "
                                    "las cuentas capitalizan diariamente."),
        ("Créditos de vivienda", "Tasas en pesos expresadas en E.A., convertidas a mes vencido; sistema de cuota fija "
                                 "mensual. No se modelan créditos en UVR ni seguros obligatorios."),
        ("Capacidad de pago", "La cuota no debe superar el 30 % del ingreso del hogar."),
        ("Clasificación VIS", "Vivienda con valor menor o igual al tope en SMMLV (editable, 135 SMMLV por defecto)."),
        ("Retención en la fuente", "CDT: 4 % sobre los rendimientos. Cuentas de ahorro: 7 % cuando el rendimiento "
                                   "diario supera 0,055 UVT. Parámetros editables."),
        ("ETF VOO", "Rentabilidad y devaluación constantes por escenario, capitalización mensual, dividendos "
                    "reinvertidos después de la retención de EE. UU.; no incluye impuesto de renta en Colombia."),
        ("Gastos de vivienda", "Avalúo y estudio de títulos estimados (editables). Escrituración: 0,15 % notaría "
                               "comprador, 1 % impuesto de registro y 0,5 % derechos de registro sobre el valor."),
    ], columns=["Tema", "Supuesto"]))
    seccion("Fuentes de los datos")
    tabla(pd.DataFrame([
        ("FNA - tasas crédito hipotecario en pesos por rango salarial (cesantías 10,00 / 12,10 / 12,60 %; "
         "AVC 11,50 / 13,10 / 13,60 %)", "fna.gov.co/transparencia/informacion-entidad/tasas", FECHA_CONSULTA),
        ("FNA - tasa preferencial UVR+0 % VIP, UVR+4,5 % VIS, LTV 100 % VIS/VIP", "fna.gov.co/personas/vivienda/tasa-preferencial",
         FECHA_CONSULTA),
        ("FNA - Generación FNA: -0,5 p.p. para 18 a 28 años; sin cobro de avalúo ni estudio de títulos",
         "portafolio.co (boletines FNA 2026)", FECHA_CONSULTA),
        ("Banco Caja Social - tasa promedio ponderada vivienda en pesos VIS 13,6 % y No VIS 14,0 %",
         "Superintendencia Financiera, corte 10-jul-2026 (vía noticiascaracol.com)", FECHA_CONSULTA),
        ("Banco Caja Social - menor tasa en proyectos financiados por el banco que en usada (diferencia de 1 p.p.)",
         "Comunicado del banco reportado por eltiempo.com y larepublica.co", FECHA_CONSULTA),
        ("CDT Nu - tasas por plazo vigentes desde el 06-oct-2026 (360 días: 11,05 % E.A.)",
         "cdn.nubank.com.br/colombia/cdt/CDT-Nu-VTUP.pdf", FECHA_CONSULTA),
        ("Cajitas Nu - hasta 11,25 % E.A. desde el 09-abr-2026", "enter.co", FECHA_CONSULTA),
        ("CDT Bancolombia 360 días: 11,66 % E.A.", "Superintendencia Financiera, corte 23-jul-2026 (vía noticiascaracol.com)",
         FECHA_CONSULTA),
        ("Cuenta de ahorros Bancolombia: 0,05 % E.A.", "finanzasplus.co, tarifario Bancolombia (verificado 18-ago-2026)",
         FECHA_CONSULTA),
        ("Retención en la fuente: 4 % CDT y 7 % cuentas de ahorro", "valoraanalitik.com (art. 395 E.T.)", FECHA_CONSULTA),
        ("TRM 21-oct-2026: $ 3.163,76", "portafolio.co / Superintendencia Financiera", FECHA_CONSULTA),
        ("VOO: expense ratio 0,03 %, rentabilidades NAV 1, 3, 5 y 10 años", "Ficha técnica Vanguard al 30-jun-2026",
         FECHA_CONSULTA),
        ("VOO: rendimiento por dividendos 1,06 %", "walnutinvest.com (Yahoo Finance, oct-2026)", FECHA_CONSULTA),
        ("SMMLV 2026: $ 1.750.905; UVT 2026: $ 52.374", "Documentos de tarifas Nu Colombia", FECHA_CONSULTA),
    ], columns=["Dato", "Fuente", "Fecha de consulta"]))
    nota("Las tasas publicadas cambian con frecuencia. Todos los valores son editables en cada módulo para "
         "actualizar el análisis el día de la presentación.")
    seccion("Verificaciones incluidas")
    tabla(pd.DataFrame([
        ("Interés simple", "Suma manual de intereses diarios contra I = P·i·t"),
        ("Interés compuesto", "numpy_financial.fv contra P(1+i)^n"),
        ("Tasas", "Conversión de ida y vuelta E.A. → mensual → E.A."),
        ("Series uniformes", "numpy_financial.pv vencida y anticipada contra fórmulas"),
        ("Gradientes", "Suma descontada cuota a cuota y numpy_financial.npv contra fórmulas"),
        ("Amortización", "Suma de abonos = capital, saldo final cero, numpy_financial.pmt"),
        ("Caso 1", "Cierre de la tabla y planes de ahorro que alcanzan la cuota inicial"),
        ("Caso 2", "Fórmula de serie y gradiente contra simulación mes a mes y numpy_financial.fv"),
        ("Caso 3", "Simulación sin costos contra la fórmula cerrada de tasa combinada"),
    ], columns=["Módulo", "Comprobación"]))
