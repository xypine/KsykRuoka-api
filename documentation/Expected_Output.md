# Expected Output & Explanation

## Explanation of keys & values

While most of the json values have quite descritptive names, the following block tries to explain as many of the possible values as possible.

> app_source:	String containing the link to the respective application repo

> app_version:	An integer representation of the app version

> menu:	should contain a list with an entry for every day of the week, where the first entry is for monday and the last is for friday. Multiple entries for a single day have been separated with \n

> menu_last_updated:	A Unix timestamp of when the menu was last updated. (float)

> menu_source_site:	A String url pointing at the site where the menu-data was scraped from.

> menu_time_since_last_update:	A float value of the time between the current time and the time the menu was last updated, essentially "time - menu_last_updated".

> menu_update_threshold:	How much time needs to pass before the api re-scrapes the menu upon the next api-request. (float)

> recent_query_count:	How many times the program has been queried since it was started. (integer)

> sheet_docs_name:	The name of the gsheet scraped for split-data. (String)

> sheets_enabled:	Is sheetscraping data avaible?

> sheets_last_updated:	A Unix timestamp of when the split-data was last updated. (float)

> sheets_lower_splitLunch:	If sheets_enabled is true, contains 5 arrays (one for each day). Each array contains all the lower-secondary classes and teachers who have a split on that corresponding day.

> sheets_normalLunch:	If sheets_enabled is true, contains 5 arrays (one for each day). Each array contains either all the upper-secondary classes and teachers who have a normal lunch on that corresponding day or "Assessmentweek", if it is assesment week.

> sheets_splitLunch:	If sheets_enabled is true, contains 5 arrays (one for each day). Each array contains either all the upper-secondary classes and teachers who have a split on that corresponding day or "Assessmentweek", if it is assesment week.

> sheets_tab_name:	Name of the gsheet tab the API scrapes split-data from. (String)

> sheets_time_since_last_update:	A float value of the time between the current time and the time the split-data was last updated, essentially "time - sheets_last_updated".

> sheets_update_threshold:	How much time needs to pass before the api re-scrapes the split-data upon the next api-request. (float)

See [example output](#Example output)  below for examples.

## Example output

A running instance of the API should output something along the following block when either a GET or a POST request is sent to the listening port of the application (defaults to :5000 and :80 on heroku):

	{
	  "app_source": "https://github.com/jonnelafin/KsykRuoka-api",
	  "app_version": 5,
	  "menu": [
	    "Kasviswokkia / Vegetable wok  (*, A, G, L, M, Veg) \n Kalkkunaa ja vihanneksia kookoskastikkeessa / Turkey and vegetable in coconut sauce  (*, A, G, L, M, VS) \n Täysjyvä riisiä / Whole grain rice  (*, G, L, M, Veg)",
	    "Kasvis-hernekeittoa / Vegetarian pea soup  (*, A, G, L, M, Veg) \n Hernekeittoa / Pea soup  (*, A, G, L, M)   contains pork \n Raejuustosalaatti / Cottage cheese salad  (*, A, G, VL) \n Pannukakkua / Pancake  (A, L) \n Hilloa / Jam  (G, L, M, Veg)",
	    "Punajuuripihvejä / Beetroot steaks  (A, G, L, M, Veg) \n Kalamurekepihvejä / Fish patties  (A, L) \n Tillikermaviilikastiketta / Sour cream sauce with dill  (A, G, L) \n Perunasosetta / Mashed potatoes  (*, A, G, L)",
	    "Beanitlasagnettea / Beanit lasagnette  (*, A, L, M, Veg, VS) \n Jauhelihalasagnettea / Minced meat lasagnette  (*, A, L)",
	    "Itämaista soija-papupataa / Bean stew with soy  (*, A, G, L, M, Veg) \n Broileri-tomaattikastiketta / Chicken and tomato sauce  (*, A, L) \n Täysjyvänuudeleita / Whole grain noodles  (*, A, L, M)"
	  ],
	  "menu_last_updated": 1601901323.8799708,
	  "menu_source_site": "https://ksyk.fi",
	  "menu_time_since_last_update": 536.2102980613708,
	  "menu_update_threshold": 3600,
	  "recent_query_count": 2,
	  "sheet_docs_name": "<SpreadSheet 1zGxZ...cM 'Kopio: Special Arrangement Lunches Period One  20-21 (13.08.2020 - 05.10.2020)'>",
	  "sheets_enabled": true,
	  "sheets_last_updated": 1601901690.2992024,
	  "sheets_lower_splitLunch": [
	    [
	      "OPO3.A (SNe)",
	      "YH1.B (AVä) ",
	      "ÄI5.C (STa)",
	      "TE3.D (TRa)",
	      "BI3.E (CFr)",
	      "BI3.F (KaH)"
	    ],
	    [
	      "xLop1.4 ABI (JSy)",
	      "xLmaa 14.3 (SSn)",
	      "xLke02.3 (EMa)",
	      "xLke02.1 (HHu)",
	      "xLke02.1 (HHu)",
	      "xLps03.1 (LLa)"
	    ],
	    [
	      "xLäi08.4 (TLy)",
	      "xLmaa14.1f (HNo)",
	      "xLyh02.3f (VKo)",
	      "xLena05.2 (PSk)",
	      "xLena05.5 (RKo)"
	    ],
	    [
	      "xLmaa07.1f (HNo)",
	      "xLrua04.1 (MiV)",
	      "xLrub04.3 (MPa)",
	      "xLena01.1 (RKo)",
	      "xLena01.3 (PSk)"
	    ],
	    [
	      "xLrub04.1 (AKa)",
	      "xLmaa07.4f (JHu)",
	      "xLrub04.2 (MPa)",
	      "xLfy01.6ef (MSl)",
	      "xLbi01.4f (CFr)"
	    ]
	  ],
	  "sheets_normalLunch": [
	    [
	      "Assessmentweek"
	    ],
	    [
	      "xLmaa02.5 (LEk)",
	      "xLeaa01.1 / eab203.1 / eab305.1 (APo)",
	      "xLrub01.3 (MPa)",
	      "xLge02.1 (MMe)",
	      "xLlt / lp02.1 mix(RKi)",
	      "xLmu02.1 (MMc)",
	      "xLyh03.5 (ATa)",
	      "xLbi08.1 (MIi)"
	    ],
	    [
	      "xLs206.1 (MAl)",
	      "xLäi06.3 (HTe)",
	      "xLhi01.4ef (SHi)",
	      "xLge01.5ef (MMe)",
	      "xLte01.1f (SLa)"
	    ],
	    [
	      "xLhi01.5ef (SHi)",
	      "xLmaa07.5ef (LEk)",
	      "xLrub04.4 (AKa) ",
	      "xLrua07.1 (PAu)",
	      "xLmaa07.3f (SSn)",
	      "xLge01.4ef (MMe)"
	    ],
	    [
	      "xLmaa07.2f (HNo)",
	      "xLue02.2f (NMä)",
	      "xLhi03.1f (ATa)",
	      "xLäi06.2 (HTe)",
	      "xLmu01.1e (MMc)",
	      "xLke01.5ef (HHu)"
	    ]
	  ],
	  "sheets_splitLunch": [
	    [],
	    [
	      "xLmaa02.1 (JHu)",
	      "xLmaa02.3 (HNo)",
	      "xLsaa01.1 (JSn)",
	      "xLraa01.1 (OVi)",
	      "xLhi06.2 (SHi)",
	      "xLeab310.1 / eaa05.1 / eab208.1 (RWe)"
	    ],
	    [
	      "xLte01.4ef (OVi)",
	      "xLps01.1f (MiV)",
	      "xLps01.3f (LLa)",
	      "xLena02.2 (PAu)",
	      "xLfy07.2ef (JMa)"
	    ],
	    [
	      "xLyh03.3fe (VKo)",
	      "xLäi08.2 (HTe)",
	      "xLmaa14.2f (EHä)",
	      "xLäi06.4 (JJu) ",
	      "xLfy07.1f (JMa)",
	      "xLäi01.2 (TLy)"
	    ],
	    [
	      "xLhi06.1ef (SHi)",
	      "xLmab08.1fe (EMa)",
	      "xLmaa14.4f (SSn)",
	      "xLäi09.5 (JJu)",
	      "xLku01.2e (EPe)",
	      "xLku01.3e (KEs)"
	    ]
	  ],
	  "sheets_tab_name": "<WorkSheet 1095636878 'Special Arrangement Lunches week 41(5.10 - 9.10)' (88x2)>",
	  "sheets_time_since_last_update": 169.79109263420105,
	  "sheets_update_threshold": 3600
	}