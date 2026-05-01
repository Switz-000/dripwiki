---
fields:
  - name: native_name
    type: Input
    options: {}
    path: ""
    id: FD6DmF
    command:
      id: insert__FD6DmF
      icon: user
      label: Insert native_name field
  - name: lusitanized_name
    type: Input
    options: {}
    path: ""
    id: gIhhzJ
  - name: aliases
    type: Multi
    options: {}
    path: ""
    id: hK2mNp
  - name: enhanced
    type: Boolean
    options: {}
    path: ""
    id: jL3nQr
  - name: demographics
    type: Object
    options:
      displayTemplate: ""
    path: ""
    id: DEMOG0
  - name: sex
    type: Select
    options:
      sourceType: ValuesList
      valuesList:
        "1": Male
        "2": Female
        "3": Unknown
    path: DEMOG0
    id: xTbTyt
  - name: ethnicity
    type: Input
    options: {}
    path: DEMOG0
    id: mN4oSt
  - name: religion
    type: Input
    options: {}
    path: DEMOG0
    id: pO5pUv
  - name: citizenship
    type: Multi
    options: {}
    path: DEMOG0
    id: qP6qVw
  - name: nationality
    type: Multi
    options: {}
    path: DEMOG0
    id: rQ7rWx
  - name: birth
    type: Object
    options:
      displayTemplate: ""
    path: ""
    id: BIRTH0
  - name: year
    type: Number
    options: {}
    path: BIRTH0
    id: sR8sXy
  - name: city
    type: Input
    options: {}
    path: BIRTH0
    id: tS9tYz
  - name: state
    type: Input
    options: {}
    path: BIRTH0
    id: uT0uZa
  - name: country
    type: Input
    options: {}
    path: BIRTH0
    id: vU1vAb
  - name: death
    type: Object
    options:
      displayTemplate: ""
    path: ""
    id: DEATH0
  - name: year
    type: Number
    options: {}
    path: DEATH0
    id: wV2wBc
  - name: city
    type: Input
    options: {}
    path: DEATH0
    id: xW3xCd
  - name: state
    type: Input
    options: {}
    path: DEATH0
    id: yX4yDe
  - name: country
    type: Input
    options: {}
    path: DEATH0
    id: zA5zEf
  - name: cause
    type: Input
    options: {}
    path: DEATH0
    id: aB6aFg
  - name: spouse
    type: Input
    options: {}
    path: ""
    id: bC7bGh
  - name: children_count
    type: Number
    options: {}
    path: ""
    id: cD8cHi
  - name: education
    type: ObjectList
    options:
      displayTemplate: ""
      itemDisplayTemplate: ""
    path: ""
    id: EDUCA0
  - name: degree
    type: Input
    options: {}
    path: EDUCA0
    id: dE9dIj
  - name: institution
    type: Input
    options: {}
    path: EDUCA0
    id: eF0eJk
  - name: year
    type: Number
    options: {}
    path: EDUCA0
    id: fG1fKl
  - name: occupation
    type: ObjectList
    options:
      displayTemplate: ""
      itemDisplayTemplate: ""
    path: ""
    id: OCCUP0
  - name: title
    type: Input
    options: {}
    path: OCCUP0
    id: gH2gLm
  - name: start_year
    type: Number
    options: {}
    path: OCCUP0
    id: hI3hMn
  - name: end_year
    type: Number
    options: {}
    path: OCCUP0
    id: iJ4iNo
  - name: military_service
    type: ObjectList
    options:
      displayTemplate: ""
      itemDisplayTemplate: ""
    path: ""
    id: MILIT0
  - name: allegiance
    type: Input
    options: {}
    path: MILIT0
    id: jK5jOp
  - name: branch
    type: Input
    options: {}
    path: MILIT0
    id: kL6kPq
  - name: rank
    type: Input
    options: {}
    path: MILIT0
    id: lM7lQr
  - name: start_year
    type: Number
    options: {}
    path: MILIT0
    id: mN8mRs
  - name: end_year
    type: Number
    options: {}
    path: MILIT0
    id: nO9nSt
  - name: conflicts
    type: Multi
    options: {}
    path: MILIT0
    id: oP0oTu
  - name: notes
    type: Input
    options: {}
    path: MILIT0
    id: pQ1pUv
  - name: political_alignment
    type: Multi
    options: {}
    path: ""
    id: qR2qVw
  - name: party
    type: Input
    options: {}
    path: ""
    id: rS3rWx
  - name: parties
    type: Multi
    options: {}
    path: ""
    id: sT4sXy
  - name: organizations
    type: Multi
    options: {}
    path: ""
    id: tU5tYz
  - name: offices
    type: ObjectList
    options:
      displayTemplate: ""
      itemDisplayTemplate: ""
    path: ""
    id: OFFIC0
  - name: title
    type: Input
    options: {}
    path: OFFIC0
    id: uV6uZa
  - name: employer
    type: Input
    options: {}
    path: OFFIC0
    id: vW7vAb
  - name: start_year
    type: Number
    options: {}
    path: OFFIC0
    id: wX8wBc
  - name: end_year
    type: Number
    options: {}
    path: OFFIC0
    id: xY9xCd
  - name: appointer
    type: Input
    options: {}
    path: OFFIC0
    id: yZ0yDe
  - name: parties
    type: Multi
    options: {}
    path: OFFIC0
    id: zA1zEf
  - name: notes
    type: Input
    options: {}
    path: OFFIC0
    id: aB2aFg
  - name: written_works
    type: ObjectList
    options:
      displayTemplate: ""
      itemDisplayTemplate: ""
    path: ""
    id: WORKS0
  - name: title
    type: Input
    options: {}
    path: WORKS0
    id: bC3bGh
  - name: publication_year
    type: Number
    options: {}
    path: WORKS0
    id: cD4cHi
  - name: genre
    type: Select
    options:
      sourceType: ValuesList
      valuesList:
        "1": Philosophy
        "2": Fiction
        "3": Non-fiction
        "4": Memoir
        "5": Poetry
        "6": Essay
    path: WORKS0
    id: dE5dIj
  - name: notes
    type: Input
    options: {}
    path: WORKS0
    id: eF6eJk
  - name: awards
    type: ObjectList
    options:
      displayTemplate: ""
      itemDisplayTemplate: ""
    path: ""
    id: AWARD0
  - name: title
    type: Input
    options: {}
    path: AWARD0
    id: fG7fKl
  - name: awarded_year
    type: Number
    options: {}
    path: AWARD0
    id: gH8gLm
  - name: posthumous
    type: Boolean
    options: {}
    path: AWARD0
    id: hI9hMn
  - name: granted_by
    type: Input
    options: {}
    path: AWARD0
    id: iJ0iNo
  - name: country
    type: Input
    options: {}
    path: AWARD0
    id: jK1jOp
  - name: notes
    type: Input
    options: {}
    path: AWARD0
    id: kL2kPq
  - name: criminal_charges
    type: ObjectList
    options:
      displayTemplate: ""
      itemDisplayTemplate: ""
    path: ""
    id: CRIMI0
  - name: charge
    type: Input
    options: {}
    path: CRIMI0
    id: lM3lQr
  - name: counts
    type: Number
    options: {}
    path: CRIMI0
    id: mN4mRs
  - name: plea
    type: Select
    options:
      sourceType: ValuesList
      valuesList:
        "1": Guilty
        "2": Not Guilty
        "3": No Contest
        "4": Alford
    path: CRIMI0
    id: nO5nSt
  - name: verdict
    type: Select
    options:
      sourceType: ValuesList
      valuesList:
        "1": Guilty
        "2": Not Guilty
        "3": Hung Jury
        "4": Mistrial
        "5": Dismissed
    path: CRIMI0
    id: oP6oTu
  - name: sentence
    type: Input
    options: {}
    path: CRIMI0
    id: pQ7pUv
  - name: served
    type: Number
    options: {}
    path: CRIMI0
    id: qR8qVw
  - name: in_absentia
    type: Boolean
    options: {}
    path: CRIMI0
    id: rS9rWx
  - name: notes
    type: Input
    options: {}
    path: CRIMI0
    id: sT0sXy
  - name: known_for
    type: ObjectList
    options:
      displayTemplate: ""
      itemDisplayTemplate: ""
    path: ""
    id: KNOWN0
  - name: item
    type: Input
    options: {}
    path: KNOWN0
    id: tU1tYz
  - name: notes
    type: Input
    options: {}
    path: KNOWN0
    id: uV2uZa
  - name: historical_period
    type: Multi
    options: {}
    path: ""
    id: vW3vAb
  - name: meta
    type: Object
    options:
      displayTemplate: ""
    path: ""
    id: META00
  - name: tags
    type: Multi
    options: {}
    path: ""
    id: wX4wBc
  - name: stub
    type: Boolean
    options: {}
    path: META00
    id: xY5xCd
  - name: verified
    type: Boolean
    options: {}
    path: META00
    id: yZ6yDe
  - name: image
    type: Input
    options: {}
    path: META00
    id: zA7zEf
  - name: summary
    type: Input
    options: {}
    path: ""
    id: Y7xlrR
version: "2.90"
limit: 20
mapWithTag: false
icon: user
tagNames:
filesPaths:
bookmarksGroups:
excludes:
extends:
savedViews: []
favoriteView:
fieldsOrder:
  - FD6DmF
  - gIhhzJ
  - hK2mNp
  - jL3nQr
  - Y7xlrR
  - DEMOG0
  - xTbTyt
  - mN4oSt
  - pO5pUv
  - qP6qVw
  - rQ7rWx
  - BIRTH0
  - sR8sXy
  - tS9tYz
  - uT0uZa
  - vU1vAb
  - DEATH0
  - wV2wBc
  - xW3xCd
  - yX4yDe
  - zA5zEf
  - aB6aFg
  - OFFIC0
  - uV6uZa
  - vW7vAb
  - wX8wBc
  - xY9xCd
  - yZ0yDe
  - zA1zEf
  - aB2aFg
  - OCCUP0
  - gH2gLm
  - hI3hMn
  - iJ4iNo
  - KNOWN0
  - tU1tYz
  - uV2uZa
  - bC7bGh
  - cD8cHi
  - EDUCA0
  - dE9dIj
  - eF0eJk
  - fG1fKl
  - qR2qVw
  - rS3rWx
  - sT4sXy
  - tU5tYz
  - MILIT0
  - jK5jOp
  - kL6kPq
  - lM7lQr
  - mN8mRs
  - nO9nSt
  - oP0oTu
  - pQ1pUv
  - WORKS0
  - bC3bGh
  - cD4cHi
  - dE5dIj
  - eF6eJk
  - CRIMI0
  - lM3lQr
  - mN4mRs
  - nO5nSt
  - oP6oTu
  - pQ7pUv
  - qR8qVw
  - rS9rWx
  - sT0sXy
  - AWARD0
  - fG7fKl
  - gH8gLm
  - hI9hMn
  - iJ0iNo
  - jK1jOp
  - kL2kPq
  - vW3vAb
  - META00
  - xY5xCd
  - yZ6yDe
  - zA7zEf
  - wX4wBc
---
