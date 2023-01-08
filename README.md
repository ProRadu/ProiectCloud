# ProiectCloud
TranslatorSite
Proiect bazat pe lucrurile facute la laborator.
Am realizat folosind free trial de la Azure.
Proiectul este impartit in:
  1)website (Pe un Vm)
      a) Pentru a functiona trebuie pornit din linie de comanda precum aplicatia BookApp facuta la laborator;
      b) ruleaza pe portul 8075;
      c) permite incarcarea intr-un container din Azure Blob Storage a unor fisier zip care contin fisiere txt;
      d) permite vizualizarea traducerilor textelor existente, acestea sunt preluate dintr-un container din Azure Cosmos DB;
  2)worker (Pe un Vm)
      a) Pentru a functiona trebuie pornit din linie de comanda;
      b) preia fisierele zip din containerul din Azure Blob Storage;
      c) citeste ce fisiere sunt deja existente in containerul corespunzator fisierelor traduse din Azure Cosmos DB;
      d) traduce textele netraduse folosind libraria gratis googletrans(4.0.0rc1 pentru ca varianta default 3.0.0 returneaza 
      o eroare cand intalneste spatii si le considera noneType);
      e) incarca textele traduse in containerul din Azure Cosmos DB structurate ca in fisiere JSON;
  3)Azure Storage Blob
      - inmagazineaza intr-un container fisierele zip incarcate de catre utilizatori
  4)Azure Cosmos Db
      - inmagazineaza intr-un container text traduse de catre worker;
  
  5)website Vm image
      - imagine creata pe baza Vm-ului pe care am testat website-ul;
  6)worker Vm image
      - imagine creata pe baza Vm-ului pe care am testat worker-ul;
  7)websiteScaleSet
      - pe baza imaginii website-ului a fost creat un scale set;
  8)website Load Balancer
      - load balancer care distribuie traficul venit catre ip-ul public catre masinile din scale set;
  9)worker Scale Set
      - pe baza imaginii worker-ului a fost creat un scale set;
  10)worker Load Balancer
      - load balancer care gestioneaza masinile din scale set in momentul in care ar fi prea multe fisiere care trebuie 
      traduse si masinile sunt suprasoliciate;
   
   In momentul testarii load balancer-elor catre scale seturi se observa ca desi era doar o masina pornita in fiecare scale set conform planului de idle, 
   nu se putea accesa site-ul nici pe ip-ul public al load balancerului, nici specificand portul 8075 dupa ip. In cazul load balancer-ului de worker
   se observa ca nu efectueaza traducei, desi, asemenea celui pentru website, mentinea doar o masina pornita in scale set in idle.
   Atat in cazul scale set-ului website-ului, cat si in cel al scale setu-ului worker-ului am completat zona de custom commands in momentul creari lor 
   pentru a trimite comenzile de activare a enverioment-urilor si a rularii fisierelor .py, dar se pare ca tot nu au pornit nici fisierul site-ului, nici
   fisierul worker-ului.
   Cum subscriptia de free trial permite doar 3 ip-uri publice, am sters load balancer-ul si scale set-ul pentru worker pentru a avea activ pe cont
   in momentul prezentarii cele 2 Vm de Demo pentru a arata functionalitatea site-ului si workerului.
   
  In fisierele incarcate aici vor fi inlocuite cu variabile dummy linkurile si cheile de acces catre Azure din motive de securitate.
   
   
