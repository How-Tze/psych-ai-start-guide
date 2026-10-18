-- Presentation-only entry. The source fingerprint identifies wording, not a release tag.
function Meta(meta)
  if not quarto.doc.is_format("html:js") then return end
  local project = pandoc.utils.stringify(meta["author-workbench-project"] or "")
  if project ~= "handbook" and project ~= "guide" then return end
  local file = assert(io.open(quarto.doc.input_file, "rb"))
  local source = file:read("*all"):gsub("\r\n", "\n")
  file:close()
  local page = pandoc.path.make_relative(quarto.doc.input_file, quarto.project.directory):gsub("\\", "/"):gsub("%.qmd$", ".html")
  quarto.doc.add_html_dependency({
    name = "psych-author-entry", version = "0.1.1",
    scripts = {{path = "author-entry.js", attribs = {defer = ""}}},
    stylesheets = {"author-entry.css"},
    meta = {
      ["psych-author-project"] = project,
      ["psych-author-page"] = page,
      ["psych-author-build"] = "sha1:" .. pandoc.utils.sha1(source)
    }
  })
end
