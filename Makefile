VPATH = data data/raw

.PHONY: all
all : entities geojson

.PHONY: entities
entities : data/indicator/BOOKS data/indicator/CONTROL_MONUMENT_MAPS \
     data/indicator/SURPLUS_PARCELS data/indicator/DEEP_TUNNELS \
	 data/indicator/DOSSIER data/indicator/EASEMENTS \
     data/indicator/FLAT_DRAWINGS data/indicator/INDEX_CARDS data/indicator/LICENSES \
     data/indicator/PROJECT_FILES data/indicator/RIGHT_OF_WAY data/indicator/SURVEYS \
     data/indicator/TITLES

data/raw/%.csv : data/raw/%.txt
	# Strip carriage returns/unecessary quotes and add source_file field to headers
	sed -e 's/\r//' -e '1 s/"//g' -e '1 s/$$/|source_file/' $< | in2csv -d "|" -f csv > $@

data/%.csv : data/raw/%.csv
	cp $< $@

.INTERMEDIATE : data/BOOKS.csv data/raw/BOOKS.csv
data/BOOKS.csv : data/raw/BOOKS.csv
	# Convert X to null and format ranges
	sed -e 's/X//g' $< | python data/processors/format_ranges.py section township range > $@

.INTERMEDIATE : data/SURVEYS.csv data/raw/SURVEYS.csv
data/SURVEYS.csv : data/raw/SURVEYS.csv
	# Fix the mislabelled columns in surveys
	sed -e '1 s/section/township/' -e '1 s/area/section/' $< | python data/processors/process_surveys.py > $@

.INTERMEDIATE : data/SURPLUS_PARCELS.csv data/raw/DEEP_PARCEL_+_SURPLUS.csv
data/SURPLUS_PARCELS.csv : data/raw/DEEP_PARCEL_+_SURPLUS.csv
	# Extract SurplusParcels from the merged SurplusParcel/DeepTunnel data
	csvgrep -c 1 -r "^$$" -i $< > $@

.INTERMEDIATE : data/DEEP_TUNNELS.csv
data/DEEP_TUNNELS.csv : data/raw/DEEP_PARCEL_+_SURPLUS.csv
	# Extract DeepTunnels from the merged SurplusParcel/DeepTunnel data
	csvcut -c 2,3 $< | csvgrep -c 1 -r "^$$" -i > $@

.INTERMEDIATE : data/CONTROL_MONUMENT_MAPS.csv data/raw/CONTROL_MONUMENT_MAPS.csv
data/CONTROL_MONUMENT_MAPS.csv : data/raw/CONTROL_MONUMENT_MAPS.csv
	# Split out township/section/range
	cat $< | python data/processors/process_controlmonumentmaps.py > $@

.INTERMEDIATE : data/EASEMENTS.csv data/raw/EASEMENTS.csv
data/EASEMENTS.csv : data/raw/EASEMENTS.csv
	# Extract descriptions
	cat $< | python data/processors/extract_description.py "easement number" > $@

.INTERMEDIATE : data/LICENSES.csv data/raw/LICENSES.csv
data/LICENSES.csv : data/raw/LICENSES.csv data/shapefiles/license_iga.geojson
	# Extract descriptions and add license geographies
	cat $< | python data/processors/extract_description.py "license number" |\
		python data/processors/link_survey_geometries.py $(word 2,$^) > $@

data/indicator/% : data/%.csv
	python manage.py import_data $< $(MODEL) --truncate

data/indicator/BOOKS : MODEL = Book
data/indicator/CONTROL_MONUMENT_MAPS : MODEL = ControlMonumentMap
data/indicator/SURPLUS_PARCELS : MODEL = SurplusParcel
data/indicator/DEEP_TUNNELS : MODEL = DeepTunnel
data/indicator/SURVEYS : MODEL = Survey
data/indicator/DOSSIER : MODEL = Dossier
data/indicator/EASEMENTS : MODEL = Easement
data/indicator/FLAT_DRAWINGS : MODEL = FlatDrawing
data/indicator/INDEX_CARDS : MODEL = IndexCard
data/indicator/LICENSES : MODEL = License
data/indicator/PROJECT_FILES : MODEL = ProjectFile
data/indicator/RIGHT_OF_WAY : MODEL = RightOfWay
data/indicator/SURVEYS : MODEL = Survey
data/indicator/TITLES : MODEL = Title

.PHONY: geojson
shapes : docsearch/static/geojson/township.geojson \
         docsearch/static/geojson/range.geojson \
         docsearch/static/geojson/section.geojson \
         docsearch/static/geojson/area.geojson

data/shapefiles/PLSSpolys.shp : data/shapefiles/PLSS.zip
data/shapefiles/areanumbers.shp : data/shapefiles/Areas.zip
data/shapefiles/PLSS_to_Areas.shp : data/shapefiles/PLSStoAreas.zip
data/shapefiles/PLSSpolys.shp data/shapefiles/areanumbers.shp data/shapefiles/PLSS_to_Areas.shp:
	unzip -d $(dir $@) "$<"

docsearch/static/geojson/%.geojson : data/shapefiles/PLSSpolys.shp
	ogr2ogr $@ $< -f GeoJSON -t_srs EPSG:4326 -dialect SQLite -sql "\
		SELECT \
		ST_Simplify(ST_Union(GEOMETRY), 10) AS geometry, \
		$(notdir $(basename $@)) AS $(notdir $(basename $@)) \
		FROM $(notdir $(basename $<)) \
		GROUP BY $(notdir $(basename $@)) \
	"

docsearch/static/geojson/section.geojson : data/shapefiles/PLSSpolys.shp
	ogr2ogr tmp_section.geojson $< -f GeoJSON -t_srs EPSG:4326 -dialect SQLite -sql "\
		SELECT \
		ST_Simplify(ST_Union(GEOMETRY), 10) AS geometry, \
		TOWNSHIP AS township, \
		RANGE AS range, \
		SECTN AS section \
		FROM $(notdir $(basename $<)) \
		GROUP BY township, range, section \
	"
	cat tmp_section.geojson | python data/processors/add_area_to_section.py > $@
	rm tmp_section.geojson

docsearch/static/geojson/area.geojson : data/shapefiles/PLSS_to_Areas.shp
	ogr2ogr $@ $< -f GeoJSON -t_srs EPSG:4326 -dialect SQLite -sql "\
		SELECT \
		ST_Simplify(ST_Union(GEOMETRY), 10) AS geometry, \
		AREANO AS area \
		FROM $(notdir $(basename $<)) \
		GROUP BY area \
	"
