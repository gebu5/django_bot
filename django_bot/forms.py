from django import forms
import datetime


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class TelegramAttachForm(forms.Form):
    api_key = forms.CharField(label='API KEY')
    chat_url = forms.CharField(label='CHAT URL')


class TaskForm(forms.Form):
    countries = [('', 'Select a Country                                                                '),
                 ('AFGH      ', 'AFGHANISTAN '), ('ALB       ', 'ALBANIA '), ('ALGR      ', 'ALGERIA '),
                 ('ARM       ', 'ARMENIA '), ('AZR       ', 'AZERBAIJAN '), ('BAMA', 'BAHAMAS '),
                 ('BAHR      ', 'BAHRAIN '), ('BRDO      ', 'BARBADOS '), ('BYS       ', 'BELARUS '),
                 ('BLZ       ', 'BELIZE '), ('BENN      ', 'BENIN '), ('BERM      ', 'BERMUDA '),
                 ('BOT       ', 'BOTSWANA '), ('BRNI      ', 'BRUNEI '), ('BULG      ', 'BULGARIA '),
                 ('BURK      ', 'BURKINA FASO '), ('BURM      ', 'BURMA '), ('BRND      ', 'BURUNDI '),
                 ('CAVI      ', 'CABO VERDE '), ('CBDA      ', 'CAMBODIA '), ('CAN', 'CANADA '),
                 ('CHAD      ', 'CHAD '), ('CONB      ', 'CONGO (BRAZZAVILLE) '), ('COD       ', 'CONGO (KINSHASA) '),
                 ('IVCO      ', 'COTE D`IVOIRE '), ('HRV       ', 'CROATIA '),
                 ('CUR', 'CURACAO '), ('CYPR      ', 'CYPRUS '), ('CZEC      ', 'CZECH REPUBLIC '),
                 ('DEN       ', 'DENMARK '), ('DJI       ', 'DJIBOUTI '), ('EGN       ', 'EQUATORIAL GUINEA '),
                 ('ERI       ', 'ERITREA '), ('SZLD      ', 'ESWATINI '), ('ETH       ', 'ETHIOPIA '),
                 ('FSM       ', 'FEDERATED STATES OF MICRONESIA '), ('FIJI      ', 'FIJI '),
                 ('FIN       ', 'FINLAND '), ('GABN      ', 'GABON '), ('GRZ       ', 'GEORGIA '),
                 ('GER       ', 'GERMANY '), ('GHAN      ', 'GHANA '), ('GNEA', 'GUINEA '), ('GUY       ', 'GUYANA '),
                 ('HAT       ', 'HAITI '), ('HNK       ', 'HONG KONG S. A. R. '), ('ICLD      ', 'ICELAND '),
                 ('IDSA      ', 'INDONESIA '), ('IRAQ      ', 'IRAQ '), ('ITLY      ', 'ITALY '),
                 ('JAM       ', 'JAMAICA '), ('JPN       ', 'JAPAN '), ('JORD      ', 'JORDAN '),
                 ('KAZ       ', 'KAZAKHSTAN '), ('KUWT      ', 'KUWAIT '), ('KGZ       ', 'KYRGYZSTAN '),
                 ('LAOS      ', 'LAOS '), ('LES       ', 'LESOTHO '), ('LBYA      ', 'LIBYA '),
                 ('LITH      ', 'LITHUANIA '), ('LXM', 'LUXEMBOURG '), ('MADG      ', 'MADAGASCAR '),
                 ('MALW      ', 'MALAWI '), ('MALI      ', 'MALI '), ('MLTA      ', 'MALTA '),
                 ('MAUR      ', 'MAURITANIA '), ('MRTS      ', 'MAURITIUS '), ('MONG      ', 'MONGOLIA '),
                 ('MTG       ', 'MONTENEGRO '), ('MORO      ', 'MOROCCO '), ('MOZ       ', 'MOZAMBIQUE '),
                 ('NAMB      ', 'NAMIBIA '), ('NETH      ', 'NETHERLANDS '), ('NZLD      ', 'NEW ZEALAND '),
                 ('NIR       ', 'NIGER '), ('NRA       ', 'NIGERIA '), ('NORW      ', 'NORWAY '),
                 ('OMAN      ', 'OMAN '), ('PNG       ', 'PAPUA NEW GUINEA '), ('POL       ', 'POLAND '),
                 ('PORT      ', 'PORTUGAL '), ('QTAR      ', 'QATAR '), ('PALA', 'REPUBLIC OF PALAU '),
                 ('RMI       ', 'REPUBLIC OF THE MARSHALL ISLANDS '), ('RUS       ', 'RUSSIA '),
                 ('RWND      ', 'RWANDA '), ('SLEO      ', 'SIERRA LEONE '), ('SING      ', 'SINGAPORE '),
                 ('SVK       ', 'SLOVAKIA '), ('SVN       ', 'SLOVENIA '), ('SSDN', 'SOUTH SUDAN '),
                 ('SRL       ', 'SRI LANKA '), ('SUDA      ', 'SUDAN '), ('SURM      ', 'SURINAME '),
                 ('SWDN      ', 'SWEDEN '), ('SYR       ', 'SYRIA '), ('TJK       ', 'TAJIKISTAN '),
                 ('TAZN      ', 'TANZANIA '), ('TMOR', 'TIMOR-LESTE '), ('TOGO', 'TOGO '),
                 ('TRIN      ', 'TRINIDAD AND TOBAGO '), ('TNSA      ', 'TUNISIA '),
                 ('TKM       ', 'TURKMENISTAN '), ('UGAN      ', 'UGANDA '), ('URU       ', 'URUGUAY '),
                 ('UZB       ', 'UZBEKISTAN '), ('YEM       ', 'YEMEN '),
                 ('ZAMB      ', 'ZAMBIA '), ('ZIMB      ', 'ZIMBABWE ')]

    cities = [('KBL', 'KABUL'), ('TIA', 'TIRANA'), ('ALG', 'ALGIERS'), ('YRV', 'YEREVAN'), ('BKU', 'BAKU'),
              ('NSS', 'NASSAU'), ('MNA', 'MANAMA, BAHRAIN'), ('BG2', 'American Citizen Services, Embassy Bridgetown'),
              ('BGN', 'BRIDGETOWN CALENDAR FOR VISITOR (B1B2) VISAS'), ('MSK', 'MINSK'), ('BLZ', 'Belize'),
              ('COT', 'COTONOU'), ('HML', 'HAMILTON'), ('GAB', 'GABORONE'), ('BSB', 'BANDAR SERI BEGAWAN'),
              ('SOF', 'SOFIA'), ('OUG', 'OUAGADOUGOU'), ('RNG', 'RANGOON'), ('BUJ', 'BUJUMBURA'), ('PIA', 'PRAIA'),
              ('PHP', 'PHNOM PENH'), ('OTT', 'OTTAWA Internal ACS Appointments'), ('NDJ', 'NDJAMENA'),
              ('BRZ', 'BRAZZAVILLE'), ('KIN', 'KINSHASA'), ('ABJ', 'ABIDJAN'), ('ZGB', 'ZAGREB'), ('CRC', 'CURACAO'),
              ('NCS', 'NICOSIA'), ('PRG', 'PRAGUE'), ('CPN', 'COPENHAGEN'), ('DJI', 'DJIBOUTI'), ('MBO', 'MALABO'),
              ('ASM', 'ASMARA'), ('MBA', 'MBABANE'), ('ADD', 'ADDIS ABABA V93 / Refugee Appointment System'),
              ('KOL', 'KOLONIA'), ('SUV', 'SUVA'), ('HLS', 'HELSINKI'), ('LIB', 'LIBREVILLE'), ('TBL', 'TBILISI'),
              ('MUN', 'MUNICH'), ('ACC', 'ACCRA'),
              ('CRY', 'U.S. Embassy Conakry Non-Immigrant Visa Appointment Schedule'), ('GEO', 'GEORGETOWN'),
              ('PTP', 'PORT AU PRINCE'), ('HNK', 'HONG KONG'), ('RKJ', 'REYKJAVIK'), ('JAK', 'JAKARTA'),
              ('SRB', 'SURABAYA'), ('ERB', 'ERBIL'), ('MLN', 'Consular Agency Venice'), ('KNG', 'KINGSTON'),
              ('FKK', 'FUKUOKA'), ('NH2', 'NAHA'), ('NHA', 'NAHA'), ('SPP', 'SAPPORO'),
              ('TK2', 'TOKYO - I-130 Petitions for Immigrant Visas'), ('TKY', 'TOKYO - Nonimmigrant Visas'),
              ('KBO', ''), ('AMM', 'AMMAN'), ('ATA', 'ALMATY'), ('AST', 'NUR-SULTAN'), ('KWT', 'KUWAIT'),
              ('BKK', 'BISHKEK'), ('VNT', 'VIENTIANE'), ('MAS', 'MASERU'), ('TRP', 'TRIPOLI'), ('VIL', 'VILNIUS'),
              ('LXM', 'LUXEMBOURG'), ('ANT', 'ANTANANARIVO'), ('LIL', 'LILONGWE'), ('BAM', 'BAMAKO'),
              ('VLL', 'VALLETTA, MALTA'), ('NUK', 'NOUAKCHOTT'), ('PTL', 'PORT LOUIS'), ('ULN', 'ULAANBAATAR'),
              ('POD', 'PODGORICA'), ('CSB', 'CASABLANCA'), ('MAP', 'MAPUTO'), ('WHK', 'WINDHOEK'),
              ('AMS', 'AMSTERDAM'), ('ACK', 'AUCKLAND'), ('APA', 'AUCKLAND'), ('NMY', 'NIAMEY'), ('ABU', 'ABUJA'),
              ('LGS', 'LAGOS'), ('OSL', 'OSLO'), ('MST', 'MUSCAT'), ('PTM', 'PORT MORESBY'), ('WRW', 'WARSAW'),
              ('LSB', 'LISBON'), ('DOH', 'DOHA'), ('KOR', 'KOROR'), ('MAJ', 'MAJURO'), ('MOS', 'MOSCOW'),
              ('SPT', 'ST PETERSBURG'), ('VLA', 'VLADIVOSTOK'), ('YEK', 'YEKATERINBURG'), ('KGL', 'KIGALI'),
              ('FTN', 'FREETOWN'), ('SGP', 'SINGAPORE'), ('BTS', 'BRATISLAVA'), ('LJU', 'LJUBLJANA'), ('JBA', 'JUBA'),
              ('CLM', 'COLOMBO'), ('KHT', 'KHARTOUM'), ('PRM', 'PARAMARIBO'), ('STK', 'STOCKHOLM'),
              ('DMS', 'DAMASCUS ---- All visa services at the Embassy have been suspended until further notice --'),
              ('DHB', 'DUSHANBE'), ('DRS', 'DAR ES SALAAM'), ('DIL', 'DILI'), ('LOM', 'LOME'), ('PTS', 'PORT OF SPAIN'),
              ('TNS', 'TUNIS'), ('AKD', 'ASHGABAT'), ('KMP', 'KAMPALA'), ('MTV', 'MONTEVIDEO'), ('THT', 'TASHKENT'),
              ('SAA', 'SANAA'), ('LUS', 'LUSAKA'), ('HRE', 'HARARE'), ('KBL', 'KABUL'), ('TIA', 'TIRANA'),
              ('ALG', 'ALGIERS'), ('YRV', 'YEREVAN'), ('BKU', 'BAKU'), ('NSS', 'NASSAU'), ('MNA', 'MANAMA, BAHRAIN'),
              ('BG2', 'American Citizen Services, Embassy Bridgetown'),
              ('BGN', 'BRIDGETOWN CALENDAR FOR VISITOR (B1B2) VISAS'), ('MSK', 'MINSK'), ('BLZ', 'Belize'),
              ('COT', 'COTONOU'), ('HML', 'HAMILTON'), ('GAB', 'GABORONE'), ('BSB', 'BANDAR SERI BEGAWAN'),
              ('SOF', 'SOFIA'), ('OUG', 'OUAGADOUGOU'), ('RNG', 'RANGOON'), ('BUJ', 'BUJUMBURA'), ('PIA', 'PRAIA'),
              ('PHP', 'PHNOM PENH'), ('OTT', 'OTTAWA Internal ACS Appointments'), ('NDJ', 'NDJAMENA'),
              ('BRZ', 'BRAZZAVILLE'), ('KIN', 'KINSHASA'), ('ABJ', 'ABIDJAN'), ('ZGB', 'ZAGREB'), ('CRC', 'CURACAO'),
              ('NCS', 'NICOSIA'), ('PRG', 'PRAGUE'), ('CPN', 'COPENHAGEN'), ('DJI', 'DJIBOUTI'), ('MBO', 'MALABO'),
              ('ASM', 'ASMARA'), ('MBA', 'MBABANE'), ('ADD', 'ADDIS ABABA V93 / Refugee Appointment System'),
              ('KOL', 'KOLONIA'), ('SUV', 'SUVA'), ('HLS', 'HELSINKI'), ('LIB', 'LIBREVILLE'), ('TBL', 'TBILISI'),
              ('MUN', 'MUNICH'), ('ACC', 'ACCRA'),
              ('CRY', 'U.S. Embassy Conakry Non-Immigrant Visa Appointment Schedule'), ('GEO', 'GEORGETOWN'),
              ('PTP', 'PORT AU PRINCE'), ('HNK', 'HONG KONG'), ('RKJ', 'REYKJAVIK'), ('JAK', 'JAKARTA'),
              ('SRB', 'SURABAYA'), ('ERB', 'ERBIL'), ('MLN', 'Consular Agency Venice'), ('KNG', 'KINGSTON'),
              ('FKK', 'FUKUOKA'), ('NH2', 'NAHA'), ('NHA', 'NAHA'), ('SPP', 'SAPPORO'),
              ('TK2', 'TOKYO - I-130 Petitions for Immigrant Visas'), ('TKY', 'TOKYO - Nonimmigrant Visas'),
              ('KBO', ''), ('AMM', 'AMMAN'), ('ATA', 'ALMATY'), ('AST', 'NUR-SULTAN'), ('KWT', 'KUWAIT'),
              ('BKK', 'BISHKEK'), ('VNT', 'VIENTIANE'), ('MAS', 'MASERU'), ('TRP', 'TRIPOLI'), ('VIL', 'VILNIUS'),
              ('LXM', 'LUXEMBOURG'), ('ANT', 'ANTANANARIVO'), ('LIL', 'LILONGWE'), ('BAM', 'BAMAKO'),
              ('VLL', 'VALLETTA, MALTA'), ('NUK', 'NOUAKCHOTT'), ('PTL', 'PORT LOUIS'), ('ULN', 'ULAANBAATAR'),
              ('POD', 'PODGORICA'), ('CSB', 'CASABLANCA'), ('MAP', 'MAPUTO'), ('WHK', 'WINDHOEK'),
              ('AMS', 'AMSTERDAM'), ('ACK', 'AUCKLAND'), ('APA', 'AUCKLAND'), ('NMY', 'NIAMEY'), ('ABU', 'ABUJA'),
              ('LGS', 'LAGOS'), ('OSL', 'OSLO'), ('MST', 'MUSCAT'), ('PTM', 'PORT MORESBY'), ('WRW', 'WARSAW'),
              ('LSB', 'LISBON'), ('DOH', 'DOHA'), ('KOR', 'KOROR'), ('MAJ', 'MAJURO'), ('MOS', 'MOSCOW'),
              ('SPT', 'ST PETERSBURG'), ('VLA', 'VLADIVOSTOK'), ('YEK', 'YEKATERINBURG'), ('KGL', 'KIGALI'),
              ('FTN', 'FREETOWN'), ('SGP', 'SINGAPORE'), ('BTS', 'BRATISLAVA'), ('LJU', 'LJUBLJANA'),
              ('JBA', 'JUBA'), ('CLM', 'COLOMBO'), ('KHT', 'KHARTOUM'), ('PRM', 'PARAMARIBO'), ('STK', 'STOCKHOLM'),
              ('DMS', 'DAMASCUS ---- All visa services at the Embassy have been suspended until further notice --'),
              ('DHB', 'DUSHANBE'), ('DRS', 'DAR ES SALAAM'), ('DIL', 'DILI'), ('LOM', 'LOME'), ('PTS', 'PORT OF SPAIN'),
              ('TNS', 'TUNIS'), ('AKD', 'ASHGABAT'), ('KMP', 'KAMPALA'), ('MTV', 'MONTEVIDEO'), ('THT', 'TASHKENT'),
              ('SAA', 'SANAA'), ('LUS', 'LUSAKA'), ('HRE', 'HARARE')]


    country_ = forms.ChoiceField(label='Страна', choices=countries)
    city = forms.ChoiceField(label='Город', choices=cities)
    date = forms.DateField(label='Дата', initial=datetime.date.today,
                           widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    accounts = forms.CharField(label='Аккаунты', widget=forms.Textarea)


class TimeForm(forms.Form):
    time = forms.TimeField(widget=forms.TimeInput(format='%HH:%MM'))

