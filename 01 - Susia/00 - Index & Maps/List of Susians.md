```dataviewjs
dv.table(
  ["Name", "Birth Year", "Occupation", "Known For", "Birth Location"],
  dv.pages()
    .where(p => {
      const nat = Array.isArray(p.nationality)
        ? p.nationality
        : p.nationality ? [p.nationality] : []

      return p.type === "person" &&
             nat.some(n => typeof n === "string" && n.includes("Susia"))
    })
    .sort(p => p.birth_year, "desc")
    .map(p => {

      const clean = val =>
        typeof val === "string"
          ? val.replace(/\[\[|\]\]/g, "").split("|")[0]
          : ""

      const city = clean(p.birth_city)
      const state = clean(p.birth_state)

      const location =
        city && state ? `${city}, ${state}` :
        city ? city :
        state ? state :
        ""

      return [
        clean(p.full_name),
        p.birth_year,
        p.occupation,
        p.known_for,
        location
      ]
    })
)



