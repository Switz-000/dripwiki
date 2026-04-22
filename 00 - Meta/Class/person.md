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
  - name: verdict
    type: Select
    options:
      sourceType: ValuesList
      valuesList:
        "1": Guilty
        "2": Not Guilty
        "3": Acquitted
        "4": Dismissed
        "6": Pardoned
    path: DG9t8d
    id: FktkIf
  - name: plea
    type: Select
    options:
      sourceType: ValuesList
      valuesList:
        "1": Guilty
        "2": Not Guilty
        "3": No Contest
        "4": No Plea
    path: DG9t8d
    id: PxI0ug
  - name: served
    type: Input
    options: {}
    path: DG9t8d
    id: p2s0R1
  - name: in_absentia
    type: Boolean
    options: {}
    path: DG9t8d
    id: xDyU8y
  - name: notes
    type: Input
    options: {}
    path: DG9t8d
    id: RfUN7o
  - name: total_sentence
    type: Input
    options: {}
    path: ""
    id: TlUofS
  - name: offices
    type: Object
    options:
      displayTemplate: ""
    path: ""
    id: QiIJj5
  - name: title
    type: Input
    options: {}
    path: QiIJj5
    id: E8ieMD
  - name: notes
    type: Input
    options: {}
    path: QiIJj5
    id: Eg61ao
  - name: employer
    type: Input
    options: {}
    path: QiIJj5
    id: M4zzzF
  - name: start
    type: Number
    options: {}
    path: QiIJj5
    id: 0tiOoG
  - name: end
    type: Number
    options: {}
    path: QiIJj5
    id: UGUlgE
  - name: appointer
    type: Input
    options: {}
    path: QiIJj5
    id: njihot
  - name: party
    type: Input
    options: {}
    path: QiIJj5
    id: 0hYoc2
version: "2.106"
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
  - QiIJj5
  - E8ieMD
  - M4zzzF
  - 0tiOoG
  - UGUlgE
  - njihot
  - 0hYoc2
  - Eg61ao
  - TlUofS
  - xTbTyt
  - FD6DmF
  - gIhhzJ
  - DG9t8d
  - C1B5sj
  - LDM6ib
  - PxI0ug
  - xDyU8y
  - FktkIf
  - lFkjOS
  - p2s0R1
  - RfUN7o
---