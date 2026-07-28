const allFieldLabels = document.querySelectorAll("[id^='div_id_'] label")
const fieldDescriptions = {
  "Area": `
    <p>Area number that project is located in.</p
    <p>Public Land Survey System term indicating a grided system of squares no larger than 6 miles × 6 miles. The numbering of Township Areas starts in the northwest end of the county, runs east to the lake and then starts back at the west end of the county. This number also represents the first number of the Cook County Property Identification Number – PIN.</p>
    <p><a href="https://hub-cookcountyil.opendata.arcgis.com/datasets/24fd4fa810794d9cba17e135f36db92c_2/explore">Click here for an interactive map of Areas</a></p>
    <p>Note: if project contains multiple locations, duplicate entries should be made for each separate Area-Section combination.</p>
  `,
  "Section": `
    <p>Section number that project is located in.</p>
    <p>Public Land Survey System term indicating a grided subsystem of squares 1 mile × 1 mile (36 Sections = 1 Township Area). The numbering of Sections starts in the northeast corner of the Township Area, runs West to 6, then East to 12, then West to 18, and so on, back and forth, until they end with Section 36 in the southeast corner. This number represents the second number of the Property Identification Number – PIN.</p>
    <p><a href="https://hub-cookcountyil.opendata.arcgis.com/datasets/217a635972fb4dfa95411e57a57d1250_3/explore">Click here for an interactive map of Sections</a></p>
    <p>Note: if project contains multiple locations, duplicate entries should be made for each separate Area-Section combination.</p>
  `,
  "Map number": `
    <p>Do not complete for new document additions. Historical Planning and Development map numbering system for filing purposes.</p>
    <p>These numbers were written on the original drawings typically below the title blocks. The filing number sequence on the sheets is in reverse order of the drawing sheets – i.e. the last sheet of the drawing set has the lowest Map Number and the first sheet of the drawing set has the largest. Map numbers were sequential for projects that were contained in the same Area-Section drawers.</p>
  `,
  "Location": `
    <p>Official FPCC name for project location.</p>
    <p>For new entries, please refer to <a href="map.fpdcc.com">map.fpdcc.com</a> or consult with GIS team for current official preserve names. For buildings, typical naming convention is: <em>[preserve complex] – [building_name]</em> and , if applicable, <em>[grove_number]</em>.</p>
    <p>Names are not currently standardized and can change over time so be aware of this restriction when searching for records.</p>
  `,
  "Building ID": `
    <p>Unique number assigned by GIS to each building in the Forest Preserves.</p>
    <p>Please contact the GIS team if you do not know how to determine building ID or need an ID generated for a new building.</p>
  `,
  "Description": `
      <p>General description of project following the format of <em>[Activity] of [Component] for [building_name] at [complex]</em>.</p>
      <p>The <em>[building_name]</em> and <em>[preserve complex]</em> are repeated as necessary where multiple locations are encompassed in the drawings.</p>
      <p>Please note when drawings are “As-Builts” or if drawing sheets are missing. Please note if the project was done in cooperation with another entity. See below for samples of Activity & Component terms:</p>
      <ul>
        <li>Example Activity Terms: Construction, Renovation, Remodeling, Demolition, Replacement, Proposal, Layout, Installation, Testing</li>
        <li>Example Component Terms: Foundation, Walls, Roof, Plumbing, HVAC, Electrical, Landscaping, Parking Lots, Trails</li>
        <li>Example Description: Construction of Chimney at General Headquarters at Cummings Square in cooperation with Works Project Administration - As Built</li>
      </ul>
      <p>When updating historical documents, preserve names that are no longer recognized should be placed in the description text and location name should be updated to reflect current official names.</p>
  `,
  "Job number": `
    <p>Historical Planning and Development project numbering system.</p>
  `,
  "Number of sheets": `
    <p>Number of sheets in set of drawings.</p>
    <p>Please note some sets of historical drawings were improperly scanned as individual sheets. These individual sheets should be combined into their respective sets, when discovered, and the number of sheets corrected to the set total.</p>
  `,
  "Date": `
    <p>Date on the drawing sheets.</p>
  `,
  "Cross ref area": `
    <p>Do not complete for new document additions.</p>
    <p>This field is a holdover from the paper indexing of historical projects used to indicate multiple locations. Note that the area and section values need to be null for any revisions to the indexing to be saved.</p>
  `,
  "Cross ref section": `
    <p>Do not complete for new document additions.</p>
    <p>This field is a holdover from the paper indexing of historical projects used to indicate multiple locations. Note that the area and section values need to be null for any revisions to the indexing to be saved.</p>
  `,
  "Cross ref map number": `
    <p>Do not complete for new document additions.</p>
    <p>This field is a holdover from the paper indexing of historical projects used to indicate multiple locations. Note that the area and section values need to be null for any revisions to the indexing to be saved.</p>
  `,
  "Hash": undefined,
  "CAD file": `
    <p>Final CAD drawing of record can be uploaded here for archival purposes, if available.</p>
  `,
  "Source file": `
    <p>Final PDF drawing of record to be uploaded for archival purposes.</p>
  `,
}

// Create and insert all tooltip modals
for (const label of allFieldLabels) {
  const labelText = label.innerText.trim().replace("*", "")
  const fieldDivId = label.parentNode.id

  if (fieldDescriptions[labelText] == undefined) {
    continue
  }

  const tooltipStr = `
    <i class="fas fa-info-circle ml-1 edit-form-tooltip"
      data-toggle="modal"
      data-target="#${fieldDivId}_modal"
    ></i>
  `
  const modalStr = `
    <div class="modal fade" id="${fieldDivId}_modal" tabindex="-1" aria-labelledby="${fieldDivId}_modal_label" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title font-weight-bold" id="${fieldDivId}_modal_label">${labelText}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body text-break">
            ${fieldDescriptions[labelText]}
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  `
  label.insertAdjacentHTML("afterend", tooltipStr + modalStr)
}

// Prevent a11y warnings from hidden modal
document.querySelectorAll(".modal").forEach((modal) => {
  // Attach onto bootstrap's jquery custom events
  $('.modal').on('hide.bs.modal', function () {
    document.activeElement.blur()
  })
})
