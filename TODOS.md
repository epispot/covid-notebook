
# Todos

Pre-production tasks:

- [x] Add compatibility for regions that don't have FIPS codes
  - Create custom geoJSON & unique FIPS codes for each region
  - [x] Re-examine special geographic zones (e.g. territories, remaining blank spots)
- [x] Efficient memory management
  - Delete data frames after use; reload from file
- [x] Add county-specific figures
  - [x] Get historical data for each county
  - [x] Display popup with historical data
- [x] Fully prepare epispot
  - [x] Add necessary functionality to epispot v3
  - [x] Publish official release candidate: v3.0.0-rc.1
- [x] Make predictions
- [x] Add CI/CD
- [ ] Work on UI
  - [ ] Show state boundaries
  - [ ] Add option to deselect counties
  - [ ] Add option to display more data in graph
  - [ ] Allow selecting special regions (e.g. Kansas City, Northern Mariana Islands)
  - [ ] Add prediction options
- [ ] Finalize curve-fitting predictions
- [ ] Publish epispot v3
