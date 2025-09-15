---
type: "post"
aliases:
- /2006/01/old-blog-entries.html
date: "2006-01-02T00:00:00Z"
tags:
- czech
- oldblog
title: Old blog entries
---

During my converstion from Jekyll to Hugo in 2022, I have decided to skip most of my old entries. Here is a short summary of few posts which are relevant after two decades (in Czech):

== 09. 05. 2006 Příběh Davida Huffmana

Byla to výzva, jakých se denně na univerzitách a vysokých školách po celém světě urodí desítky. Profesor umožnil svým studentům vyhnout se zkoušce, když vyřeší složitý problém. Jednalo se o problém dosažitelnosti nejkratšího prefixového kódování (tzv. ideální kódování ve vztahu k informační entropii). Studenti ovšem nevěděli, že se jedná o nevyřešenou úlohu, protože v té době byly známy jen docela neúčinné metody (analýzou shora dolů).

Davidu Huffmanovi na univerzitě v Ohiu se ke zkoušce nechtělo. Ne snad proto, že by látce nerozuměl. Chtěl se jí prostě vyhnout, jenže úloha se zdála téměř neřešitelná. Když už chtěl nechat bádání a začít se na závěrečnou zkoušku učit, zadíval se na papír s poznámkami, které zlostně vyhodil do koše. V tu chvíli ho to napadlo.

Magistr Huffman později publikoval svůj nápad v práci nazvanou Metoda pro vytvoření kódu s minimální redundancí (A Method for the Construction of Minimum Redundancy Codes). Jeho řešení pomocí binárního stromu bylo velmi prosté a zároveň elegantní. Ale také velmi účinné v praxi. V tu dobu již působil na MIT (Massachusetts Institute of Technology), kde také získal rok nato doktorát.

Míru informace (přesněji řečeno nejistoty) stanovil poprvé americký vědec C. E. Shannon. Určuje nahodilost v nějakém signálu - například míru informace písmena „a“ ve větě (v řetězci písmen). Čím více se pravděpodobnost výskytu písmena na dané pozici blíží hodnotě 0,5, tím vyšší má informační hodnotu. Více prozradí tento graf - na ose x je pravděpodobnost výskytu a je jasné, že pokud se písmeno v řetězci nevyskytuje, nebo je řetězec tvořen jen tímto písmenem, pak je míra informace minimální.

Princip spočívá ve vytvoření binárního stromu s ohodnocenými hranami (1,0) a uzly (pravděpodobnosti výskytu). Pravděpodobnost vnitřního uzlu je rovna součtu pravděpodobností jeho potomků. Ve výsledném stromu jsou kódované znaky uložené pouze v listech, takže je zaručeno, že kódování (tedy posloupnost ohodnocení hran od kořene k listu) bude prefixové (tedy žádná předpona nebude kódem jiného znaku - zakódovaný vstup bude jednoznačně dekódovatelný, protože neznáme šířky binárních kódů). Doporučuji shlédnout demonstrační applet.

Dnes se nejrůznější varianty Huffmanova kódování (například adaptivní varianta) používají v široké škále produktů, zejména je to neoddělitelná součást některých komprimačních algoritmů (PKZIP, JPEG, MP3, BZIP2). Zajímavé je, že algoritmus z unixového programu bzip2 používal nejdříve aritmetické kódování (jedná se o zobecněný princip Huffmanova kódování, algoritmus vykazuje mírně vyšší účinnost). Jelikož ale na tento algoritmus získala firma IBM v letech 1977-2001 přes desítku patentů a bylo prakticky nemožné jej efektivně implementovat bez použití těchto metod, programátoři tohoto open-source programu se rozhodli použít Huffmanovo kódování.

Profesor David A. Huffman stál při zrodu fakulty informatiky na kalifornské univerzitě a získal mnoho ocenění (kromě jiného medaili R. W. Hamminga při IEEE za celoživotní přínost pro informatiku). Po desetiměsíčním boji s rakovinou v říjnu 1999 zemřel. David Huffman svůj geniální nápad nikdy nepatentoval (ani nechtěl). Svému synovci říkával: „Vždyť je to jen algoritmus.“

Článek vyšel na serveru Scienceworld.cz. (http://scienceworld.cz/technologie/pribeh-davida-huffmana-a-jeho-kodovani-1453)

== 16. 03. 2006 Schism Tracker a starý songy

Dnes se mi podařila úžasná věc - náhodou jsem narazil na stařičké CD s archivem mých starých modulů. Ve svých zhruba patnácti jsem začínal na svém stroji s procesorem Intel 386 skládat v programech Fast Tracker 2 a později Impulse Tracker (dodnes nepřekonaný) různé paskvily a náznaky muziky. Hudební vzdělání jsem neměl, ale bavilo mě to.

Vše to začalo, když jsem si do svého počítače koupil (za velký peníz) zvukovou kartu Sound Blaster 16. Byla velká asi jako dnešní špičkové grafické karty (chladič ovšem neměla), tak jsem musel celý počítač přeskládat, aby se mi tam vešla.

Vybral jsem několik skladeb, které mi nějakým způsobem přirostly k srdci. Na Linuxu si je pustíte pomocí programu mikmod (příkaz mikmod -i -X skladba). Existuje i plugin pro XMMS. Pokud byste však chtěli vidět, jak takový modul vypadá „uvnitř“, doporučuji skvělý klon Impulse Trackeru jménem Schism Tracker. Ovládá se jednoduše, po spuštění dejte F9, načtěte skladbu a klávesou F5 začnete přehrávat. Pod SHIFT-F9 jsou u některých skladeb doplňující informace, Schism můžete použít i ke skládání, ale nezkoušel jsem soubory jakkoli modifikovat. Ukázka obrazovky skládání a informací pod SHIFT-F9. Program opustíte kombinací CTRL+Q.

SDREAM.XM (Synth Dream) - prvotina když mi bylo snad 15 let, tehdy jsem neměl ještě ani stereo reproduktory. To se podepsalo na celkové mixáži, nedoporučuji pouštět na sluchátkách (levá strana hraje o poznání víc). Skladbě dominují syntetické zvuky a velmi nekvalitní bicí (8 bitů, přišerný sampling). Tohle raději nebudu škatulkovat.

INDEPENC.IT (Independence) - puberta se mnou mlátí ze strany na stranu. Tohle je stará skladba udělaná ve Fast Trackeru 2, ale den před Vánoci 1997 jsem ji předělal do legendárního Impulse Trackeru. To už jsem měl kvalitní zvukovou kartu a stereo reproduktory, což je poznat na basovém synthu linoucím se střídavě z pravé a levé strany. Prosinec roku 1997, bylo mi 17 let.

NEJJIMBL.IT (Nejlíp Jim Bylo) - doba středoškolská, páčo a Mňága a Žďorp. Předělávka hitu s falešnou kytarou a šíleními bicími, to vše doplněno mírně ujetým „ping“ synťákem. Jó, to byly časy. Začínal apríl roku 98.

EXAM.IT (Exam) - trip-hopová deep skladbička se zajímavým beatem. Hluboké basy střídají syntetické zvuky. Informace o skladbě naznačují, že jsem ji složil den před svou maturitní zkouškou. Evidentně jsem tehdy sledoval seriály Akta X a Brutální Nikita, když to v infu zmiňuji. Bylo 27. 7. 1998.

TTFM.IT (Tribute To Five Musicans) - asi nejpovedenější skladba, ale krátká. Reflektuje můj obdiv ke grupě Five Musicians (v názvu skladby mám překlep). Tito chlapíci předběhli dobu, jejich elektronika má nápad. Tento kousek zřejmě nebyl dokončen. Srpen 1998.

W8INGIF.IT (W8in` If She Wake Up) - pořádně anglicky jsem rozhodně neuměl, ale liboval jsem si v různých zkratkách (ala i18n, cryin` atd) či sprostých slovech - těch jsem uměl dost Podepsalo se to na názvu téhleté předělávky Jonathana Dunna z platformy Commodore C64 ze hry Platoon (Četa). Skladbu jsem věnoval kamarádce Veronice. Datum u tohodle modulu není (odhaduji to někdy na rok 1997).

== 22. 02. 2006 Patch v projektu Lucene

Po dlouhé době konečně vývojáři přijali můj optimalizační patch do open-source knihovny Lucene.

== 23. 12. 2005 Nokia 6230i

Tak k nám zavítal Ježíšek a přinesl mi novou Nokii 6230i. Velmi dlouho jsem používal Siemens C55 (po pádu ze schodů S55). Musím uznat, že tím telefonem jsem ohromen. Jediná výtka je ke slovníku T9, který je s diakritikou (což nevyužiji). To by samo o sobě nebylo nic zvláštního, jenže díky těmto (asi zbrklým) úpravám českého slovníku vypadly některé slovíčka, včetně například slova „Nokia“ nebo několika předložek. Ale to mě tak nebolí, T9 nepoužívám a jistě to půjde nějakým způsobem „patchnout“.

Tak, ještě pořídím svoji první fotku (no ona je vlastně čtvrtá). Připravit, pozor, cvak! No první fotka se nepovedla, tak počkám na ráno. S ránem přijde tolik potřebné denní světlo. Zdokumentoval jsem svoje pracovní prostředí a pohled na Olomouc z mého balkonu.

== 24. 10. 2005 Neuronová komprese obrázku v Pythonu

Prozkoumal jsem možnosti balíku SNNS (Stuttgart Neural Network Simulator) a jeho rozhraní v jazyce Python tak, že jsem vytvořil krátký program na vytvoření neuronové sítě a metodou Backpropagation jsem síť naučil na identické bloky o velikosti 8 x 8 pixelů z jednoho konkrétního obrázku. Po naučení jsem síti předložil postupně celý obrázek (po blocích) a zrekonstruoval výstup sítě zpět, jako obraz. Výsledkem je obrázek, který koresponduje se známými metodami ztrátové komprese pomocí neuronových sítí.

<a href="http://lukas.zapletalovi.com/papers/neuronova_komprese/">Výsledek</a>

== 31. 12. 2005 Poprvé v novinách

Dneska se poprvé v mém životě objevila moje fotka v novinách. Kulturní rubrika Olomouckého Dne sice není žádné terno, ale přesto je to poprvé. Upozorňuje na dnešní akci v U-Klubu, ve kterém budu hrát na silvestrovské trance/drumandbass party. Možná se tam uvidíme! Každopádně vše nejlejší do nového roku 2006!

