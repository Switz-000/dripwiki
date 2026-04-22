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
  - name: sex
    type: Select
    options:
      sourceType: ValuesList
      valuesList:
        "1": Male
        "2": Female
        "3": Unknown
    path: ""
    id: xTbTyt
    command:
      id: insert__xTbTyt
      icon: list-plus
      label: Insert sex field
    style:
      code: false
  - name: criminal_charges
    type: Object
    options:
      displayTemplate: ""
    path: ""
    id: DG9t8d
  - name: charge
    type: Input
    options: {}
    path: DG9t8d
    id: C1B5sj
  - name: counts
    type: Number
    options: {}
    path: DG9t8d
    id: LDM6ib
  - name: sentence
    type: Input
    options: {}
    path: DG9t8d
    id: lFkjOS
version: "2.20"
limit: 20
mapWithTag: false
icon: package
tagNames:
filesPaths:
bookmarksGroups:
excludes:
extends:
savedViews: []
favoriteView:
fieldsOrder:
  - DG9t8d
  - C1B5sj
  - LDM6ib
  - lFkjOS
  - FD6DmF
  - gIhhzJ
  - xTbTyt
---