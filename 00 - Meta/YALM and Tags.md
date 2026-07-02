
Type: What kind of article this is. Single value.
```
type: country
type: state
type: city
type: fez
type: company
type: person
type: institution
type: law
type: project
type: treaty
type: event
type: war
type: tradition
type: concept
type: movement
type: document
type: technology
type: structure
type: organization
type: religion
type: sport
type: index
type: meta
type: ideology
```

Era: What historical period the article primarily belongs to. Can take multiple values. If a person only lived like two years in the late imperial period as a baby don't bother adding them to that period. Only add war / revolts eras if a person was directly influncing it otherwise only include broader ones: post war, continental divide

Susia:
```
era:
  - pre-colonial        # Before Armotist arrival, 1651
  - settlement          # 1651–1674, first colonies
  - imperial-era #1674-1954 
	  - early-imperial      # 1674–1740, Mantichev through Agamilos
	  - high-imperial       # 1740–1837, Veronique through Jartes I
		  - fraternal-war       # 1815–1823, specific era within high imperial
	  - late-imperial       # 1837–1954, Jartes II through dissolution
		  - liberal-revolts     # 1840–1844, specific era within late imperial
		  - dissolution         # 1950–1954, Tahuni Accords and republic establishment
  - republican-era    # 1954–2038, before the great transition after the dissolution
	  - continental-divide  # 1957–1977, cold war with Confia
		  - continental-war     # 1975–1977, hot war
	  - post-war            # 1977–2006, reconstruction and boom
	  - new-age            # 2006–2038, amepur war, modernist movment
		  - great-transition   # 2036–2038, new constitution convention
  - global-cold-war     # 2006–present, Ashgerad cold war
  - techno-federative-era  # 2038–present, post great transition
	  - enhancement-era  # 2060s–present, cognitive enhancement period
	  - contemporary   # 2070s–2090s, present day of the world
```

Confia:
```
era:
	- pre-colonial # Before Racpalian colonization, 1780
	- settlement # 1786–1811, first colonies
	- imperial-era #1786-1950 
		- early-imperial # 1674–1740, Mantichev through Agamilos
		- high-imperial # 1740–1837, Veronique through Jartes I
			- fraternal-war # 1815–1823
		- late-imperial # 1837–1954, Jartes II through dissolution
			- aiding_state # 1845-1922
			- home_rule # 1922–1937, Rule from St. Mantichev City
			- secession_war # 1937-1950
			- state_of_confia # 1950-1953
			- confian_anarchy # 1954-1956
	- united_syndicates # 1956–2009, Proclamation to 2009 constitution
		- paulowic_regime # 1956–1977, Presidential Empowerment Amendment to Bayonet Revolution
			- continental-war # 1975–1977, hot war
		- syndicalist_republic # 1977–2009
	- social_republic # 2009-present 
```

Tags: What subject area the article belongs to. Can take multiple values.
```
tags:
  - politics
  - military
  - economy
  - corporate
  - law
  - journalism
  - intelligence
  - philosophy
  - religion
  - culture
  - sport
  - science
  - technology
  - medicine
  - geography
  - diplomacy
  - colonial
  - labor
  - media
  - education
  - infrastructure
  - finance
  - energy
  - agriculture
  - crime
  - immigration
  - race
  - history
```