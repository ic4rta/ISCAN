import urllib3
import os
import socket
import dns
import dns.resolver
import dns.query
import dns.zone
import dns.name
import dns.reversename
import requests
from lxml import html
from bs4 import BeautifulSoup
from urllib.parse import urlparse


# variables globales
G = "GET"
P = "POST"

# Colores
verde = '\033[32m'
rojo = '\033[31m'
brigth = '\033[1m'
blanco = '\033[37m'
normal = '\033[22m'

banner =  "  __       _______   ______      ___       __   __\n"
banner += " |  |     /       | /      |    /   \     |  \ |  |\n"
banner += " |  |    |   (----`|  ,----'   /  ^  \    |   \|  |\n"
banner += " |  |     \   \    |  |       /  /_\  \   |  . `  |\n"
banner += " |  | .----)   |   |  `----. /  _____  \  |  |\   |\n"
banner += " |__| |_______/     \______|/__/     \__\ |__| \__| v1.0\n\n"
banner += "                                  Creado por c4rta\n"


# inputs
while True:
    dominio = str(input("Ingrese el dominio sin HTTP: "))
    metodo = str(input("Como desea relizar las peticiones (P)POST (G)GET: "))
    if "https" in dominio or "http" in dominio:
        print("Ingresa sin HTTP/HTTPS y el metodo correcto")
    else:
        os.system("clear")
        break


#funcion para obtener las imagenes de la web
def scrapingIMG(dominio):
    print(f"""\n{verde}{brigth}Obteniendo imagenes{blanco}{normal}""")
    print("-------------------")
    try:
        response = requests.get(dominio)
        parsedBody = html.fromstring(response.text)
        imagenes = parsedBody.xpath('//img/@src')
        print("Imagenes encontradas %s" % len(imagenes))

        if os.path.exists("imagenes"):
            print("La carpeta imagenes ya existe y no se creara")
        else:
            print("Creando carpeta imagenes")
            os.system("mkdir imagenes")

        for img in imagenes:
            if img.startswith("http") == False:
                descarga = dominio + img
            else:
                descarga = img
            print(descarga)

            r = requests.get(descarga)
            f = open("imagenes/%s" % descarga.split("/")[-1], "wb")
            f.write(r.content)
            f.close()
        print("-------------------")
    except Exception as e:
        print(f"""{rojo}{brigth}Error al descargar imagenes{blanco}{normal}""", e)
        pass


#funcion para obtener los PDF de la web
def scrappingPDF(dominio):
    print(f"""\n{verde}{brigth}\nObteniendo PDFS{blanco}{normal}""")
    try:
        response = requests.get(dominio)
        parsedBody = html.fromstring(response.text)
        pdf = parsedBody.xpath('//a[@href[contains(., ".pdf")]]/@href')
        if len(pdf) > 0:
            os.system("mkdir pdfs")

        print("PDF encontrados %s" % len(pdf))
        for pdfs in pdf:
            if pdfs.startswith("http") == False:
                descagar = dominio + pdfs
            else:
                descagar = pdfs

            r = requests.get(descagar)
            f = open("pdfs%s" % descagar.split('/')[-1], "wb")
            f.write(r.content)
            f.close()
        print("-----------------")
    except Exception as e:
        print(f"""{rojo}{brigth}Error al descargar PDF{blanco}{normal}""", e)
        pass


#Funcion para obtener los links de la web
def scrappingLinks(dominio):
    print(f"""\n{verde}{brigth}\nObteniendo links{blanco}{normal}""")
    print("-------------------")

    try:
        response = requests.get(dominio)
        parsedBody = html.fromstring(response.text)
        links = parsedBody.xpath('//a/@href')

        print("Links encontrados %s" % len(links))

        for link in links:
            print(link)
        print("-------------------")
    except Exception as e:
        print(f"""{rojo}{brigth}Error al obtener links{blanco}{normal}""")
        pass


#Obtener la IP de la web
def ip(dominio):
    try:
        ip = socket.gethostbyname(dominio)
        return ip
    except socket.error as error:
        print(f"""{rojo}{brigth}Error de conexion{blanco}{normal}""")


#Obtener las cabeceras HTTP
def cabeceras(metodo, dominio):
    pool = urllib3.PoolManager(10)
    response = pool.request(metodo, dominio)
    if response.status != 200:
        print(f"""{rojo}{brigth}ERROR - NO SE PUDO REALIZAR LA PETICION{blanco}{normal}""")
    else:
        response.headers.keys()
        response.headers.values()
        os.system("clear")
        print(f"""{verde}{brigth}Las cabeceras son:{blanco}{normal}""")
        print("------------------\n")
        for header, valor in response.headers.items():
            print(header + ":" + valor)


#Obtener los servidores DNS
def servidoresDNS(dominio):
    os.system("clear")
    resol = dns.resolver.Resolver()
    try:
        ansMX = (resol.resolve(dominio, 'MX'))
        print(f"""\n\n{verde}{brigth}Servidores de correo{blanco}{normal}""")
        print("--------------------")
        for correo in ansMX:
            print(correo.to_text())
    except dns.resolver.NoAnswer:
        print(f"""{rojo}{brigth}No se encontraron{blanco}{normal}""")

    try:
        print(f"""\n{verde}{brigth}Servidores de nombre{blanco}{normal}""")
        print("----------------------")
        ansNS = (resol.resolve(dominio, 'NS'))
        for nombre in ansNS:
            print(nombre.to_text())
    except dns.resolver.NoAnswer:
        print(f"""{rojo}{brigth}No se encontraron{blanco}{normal}""")

    try:
        print(f"""\n{verde}{brigth}Servidores IPv4{blanco}{normal}""")
        print("-----------------")
        ansA = (resol.resolve(dominio, 'A'))
        for ipv4 in ansA:
            print(ipv4.to_text())
    except dns.resolver.NoAnswer:
        print(f"""{rojo}{brigth}No se encontraron{blanco}{normal}""")

    try:
        print(f"""\n{verde}{brigth}Servidores de administracion de dominio{blanco}{normal}""")
        print("-----------------------------------------")
        ansSOA = (resol.resolve(dominio, 'SOA'))
        for soa in ansSOA:
            print(soa.to_text())
    except dns.resolver.NoAnswer:
        print(f"""{rojo}{brigth}No se encontraron{blanco}{normal}""")

    try:
        print(f"""\n{verde}{brigth}Servidores IPv6{blanco}{normal}""")
        print("-----------------")
        ansAAAA = (resol.resolve(dominio, 'AAAA'))
        for ipv6 in ansAAAA:
            print(ipv6.to_text())
    except dns.resolver.NoAnswer:
        print(f"""{rojo}{brigth}No se encontraron{blanco}{normal}""")
    
    try:
        print(f"""\n{verde}{brigth}Servidores de registro TXT{blanco}{normal}""")
        print("----------------------------")
        ansTXT = (resol.resolve(dominio, 'TXT'))
        for txt in ansTXT:
            print(txt.to_text())
    except dns.resolver.NoAnswer:
        print(f"""{rojo}{brigth}No se encontraron{blanco}{normal}""")

    try:
        print(f"""\n{verde}{brigth}Servidores de registro CNAME{blanco}{normal}""")
        print("------------------------------")
        ansCNAME = (resol.resolve(dominio, 'CNAME'))
        for cname in ansCNAME:
            print(cname.to_text())
    except dns.resolver.NoAnswer:
        print(f"""{rojo}{brigth}No se encontraron{blanco}{normal}""")

    try:
        print(f"""\n{verde}{brigth}Servidores de registro SRV{blanco}{normal}""")
        print("----------------------------")
        ansSRV = (resol.resolve(dominio, 'SRV'))
        for srv in ansSRV:
            print(srv.to_text())
    except dns.resolver.NoAnswer:
        print(f"""{rojo}{brigth}No se encontraron{blanco}{normal}""")
    
    try:
        print(f"""\n{verde}{brigth}Servidores de registro PTR{blanco}{normal}""")
        print("----------------------------")
        ansPTR = (resol.resolve(dominio, 'PTR'))
        for ptr in ansPTR:
            print(ptr.to_text())
    except dns.resolver.NoAnswer:
        print(f"""{rojo}{brigth}No se encontraron{blanco}{normal}""")


def menu():
    print(f"""\n\n{verde}{brigth}{banner}""")
    print(f"""{blanco}{normal}IP del objetivo: """+ip(dominio))
    print("\n\n[1] Obtener Cabeceras")
    print("[2] Obtener servidores DNS")
    print("[3] Webscrapping")
    print("[4] Salir")


def main():
    while True:
        menu()
        try:
            opc = int(input("Ingrese lo que desea hacer: "))

            if opc in range(4):
                if opc == 1:
                    if metodo == "P":
                        cabeceras(P, dominio)
                    if metodo == "G":
                        cabeceras(G, dominio)

                elif opc == 2:
                    servidoresDNS(dominio)

                elif opc == 3:
                    scrapingIMG('http://'+dominio)
                    scrappingPDF('http://'+dominio)
                    scrappingLinks('http://'+dominio)
            elif opc == 4:
                break

        except ValueError:
            print("Debes de ingresa un numero")


if __name__ == "__main__":
    main()
