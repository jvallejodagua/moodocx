
--[[
--Se conserva porque puede ser útil en caso de que el filtro actual no funcione
--El código de nuestro filtro aplanador de tablas en memoria

local in_table = false

function Table(el)
  in_table = true
  local res = pandoc.walk_block(el, {
    BlockQuote = function(bq)
      return bq.content
    end
  })
  in_table = false
  return res
end
]]

local pandoc = require "pandoc"

-- 1. Función para aplanar cualquier bloque a elementos en línea
local function flatten_blocks(blocks)
  local inlines = pandoc.List()
  if not blocks then return inlines end
  
  for _, block in ipairs(blocks) do
    if block.t == 'Plain' or block.t == 'Para' then
      inlines:extend(block.content)
      inlines:insert(pandoc.Space())
    elseif block.t == 'BlockQuote' or block.t == 'Div' then
      inlines:extend(flatten_blocks(block.content))
    elseif block.t == 'BulletList' or block.t == 'OrderedList' then
      for _, item in ipairs(block.content) do
        inlines:extend(flatten_blocks(item))
      end
    elseif block.t == 'Header' then
      inlines:extend(block.content)
      inlines:insert(pandoc.Space())
    end
  end
  return inlines
end

-- 2. Procesamiento de celdas: limpieza de texto y reseteo de Spans
local function process_cell(cell)
  local inlines = flatten_blocks(cell.contents)
  local cleaned = pandoc.List()
  local skip_space = false

  for _, inl in ipairs(inlines) do
    if inl.t == 'LineBreak' or inl.t == 'SoftBreak' then
      if #cleaned > 0 and cleaned[#cleaned].t ~= 'Space' then
        cleaned:insert(pandoc.Space())
      end
    elseif inl.t == 'Str' then
      -- Eliminar símbolos de cita '>' al principio de la cadena
      local text = inl.text:gsub("^>+%s*", "")
      if text ~= "" then
        cleaned:insert(pandoc.Str(text))
        skip_space = false
      else
        skip_space = true
      end
    elseif inl.t == 'Space' then
      if not skip_space and #cleaned > 0 and cleaned[#cleaned].t ~= 'Space' then
        cleaned:insert(inl)
      end
      skip_space = false
    else
      cleaned:insert(inl)
      skip_space = false
    end
  end

  if #cleaned > 0 and cleaned[#cleaned].t == 'Space' then
    cleaned:remove(#cleaned)
  end

  -- PURGA DE PROPIEDADES: Obligatorio para Pipe Tables
  cell.contents = { pandoc.Plain(cleaned) }
  cell.col_span = 1 -- Anula celdas combinadas horizontales
  cell.row_span = 1 -- Anula celdas combinadas verticales
  
  return cell
end

local function process_row(row)
  for i, cell in ipairs(row.cells) do
    row.cells[i] = process_cell(cell)
  end
  return row
end

-- 3. Interceptar tabla y reestructurar su topología por la fuerza
function Table(tbl)
  -- A. Anular anchos fijos de columna (ColWidthDefault)
  for i, colspec in ipairs(tbl.colspecs) do
    tbl.colspecs[i] = {colspec[1], pandoc.ColWidthDefault}
  end

  -- B. Recolectar absolutamente todas las filas en una lista plana
  local all_rows = pandoc.List()

  if tbl.head and tbl.head.rows then
    for _, row in ipairs(tbl.head.rows) do all_rows:insert(process_row(row)) end
  end
  
  if tbl.bodies then
    for _, body in ipairs(tbl.bodies) do
      if body.head then
        for _, row in ipairs(body.head) do all_rows:insert(process_row(row)) end
      end
      if body.body then
        for _, row in ipairs(body.body) do all_rows:insert(process_row(row)) end
      end
    end
  end
  
  if tbl.foot and tbl.foot.rows then
    for _, row in ipairs(tbl.foot.rows) do all_rows:insert(process_row(row)) end
  end

  if #all_rows == 0 then return tbl end

  -- C. Construir arquitectura exigida por Pipe Tables (1 Head row, 1 Body, 0 Footers)
  tbl.head.rows = { all_rows[1] } -- La primera fila siempre será la cabecera
  
  local body_rows = pandoc.List()
  for i = 2, #all_rows do
    body_rows:insert(all_rows[i])
  end

  if #tbl.bodies > 0 then
    tbl.bodies[1].row_head_columns = 0 -- Anula columnas de cabecera lateral
    tbl.bodies[1].head = pandoc.List()
    tbl.bodies[1].body = body_rows
    -- Eliminar cualquier cuerpo de tabla extra
    for i = #tbl.bodies, 2, -1 do table.remove(tbl.bodies, i) end
  end

  tbl.foot.rows = pandoc.List() -- Anular pie de tabla

  return tbl
end