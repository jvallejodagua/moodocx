-- format_new_lines.lua
function Para(el)
  -- Verifica si el párrafo está completamente vacío en el AST
  if #el.content == 0 then
    return pandoc.RawBlock('html', '<br>')
  -- Opcional: Atrapa párrafos que Word haya guardado solo con un espacio en blanco
  elseif #el.content == 1 and el.content[1].t == "Space" then
    return pandoc.RawBlock('html', '<br>')
  end
  return el
end