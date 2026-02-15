```dataviewjs
dv.table(
  ["Name", "Birth Year", "Occupation", "Known For", "Birth Place"],
  dv.pages()
    .where(p => p.type === "person" && p.citizenship?.includes("Susian"))
    .sort(p => p.birth_year, "desc")
    .map(p => {
      const places = Array.isArray(p.birth_place)
        ? p.birth_place
        : p.birth_place ? [p.birth_place] : []

      const cityPlaces = places.filter(place =>
        dv.page(place.path)?.type === "city"
      )

      return [
        p.person_name,
        p.birth_year,
        p.occupation,
        p.known_for,
        cityPlaces
      ]
    })
)

