# Location-Based Filtering

## Overview
The climate chat agent now supports location-based filtering, allowing you to query data for specific countries or geographic coordinates.

## Supported Location Formats

### 1. Country Names
Simply mention a country name in your query:
```
Show me temperature data for Germany in 1950
What was the climate like in France during 1951?
Give me precipitation data for Italy
```

**Supported Countries:**
- Germany, France, Italy, Spain, UK/United Kingdom
- USA/United States, Canada, Australia
- Japan, China, India, Brazil, Mexico
- Netherlands, Belgium, Switzerland, Austria, Poland
- Norway, Sweden, Denmark, Finland
- Portugal, Greece, Ireland, Czech Republic
- (More can be added easily)

### 2. Latitude/Longitude Coordinates
Provide precise coordinates in various formats:

**Format 1: Named parameters**
```
Show temperature at lat: 52.5, lon: 13.4 in 1950
Give me data for latitude: 48.8, longitude: 2.3
```

**Format 2: Simple decimal pair**
```
What's the climate at 52.5, 13.4?
Show me data for 48.8, 2.3 in 1951
```

**Format 3: Degrees with direction**
```
Get data for 52.5°N 13.4°E
Show climate at 48.8°N, 2.3°E
```

**Coordinate Ranges:**
- Latitude: -90 to +90 (North is positive, South is negative)
- Longitude: -180 to +180 (East is positive, West is negative)

## Example Queries

### Country-Based Queries
```
1. "Show me all climate variables for Germany in 1950"
2. "What was the temperature in France during 1951?"
3. "Give me precipitation data for Italy in January 1950"
4. "Climate overview for Spain in 1950"
```

### Coordinate-Based Queries
```
1. "Temperature at lat: 52.5, lon: 13.4 in 1950"
2. "Climate data for 48.8, 2.3 during 1951"
3. "What's the weather like at 52.5°N 13.4°E?"
4. "Show me all variables at coordinates 40.7, -74.0"
```

### Combined Queries
```
1. "Temperature in Germany at lat: 52.5, lon: 13.4 in June 1950"
2. "Climate in France near 48.8, 2.3 for 1951"
```

## How It Works

### Detection
The system automatically detects location information in your queries:
1. **Country Names**: Scans for known country keywords
2. **Coordinates**: Uses regex patterns to extract lat/lon values
3. **Session Memory**: Stores location context across the conversation

### Query Processing
When location info is detected:
1. **Country Name**: Stored for context, LLM can suggest coordinate refinement
2. **Coordinates**: Stored and can be used for spatial filtering
3. **Feature URIs**: If you know specific feature URIs, they take precedence

### Templates
New SPARQL templates support location filtering:
- `location_based_summary`: Climate overview for a specific location
- `features_near_coordinates`: Lists features near given coordinates
- Existing templates can use location context when available

## Technical Details

### State Fields
- `location_name`: Detected country or place name
- `coordinates`: Dict with `lat` and `lon` keys (floats)

### Session Persistence
Location information is saved in session memory along with:
- Selected property (e.g., temperature)
- Time range (1950-1951)
- Feature URI

### Coordinate Validation
- Latitude: Must be between -90 and +90
- Longitude: Must be between -180 and +180
- Invalid coordinates are rejected with a console warning

## Limitations

1. **Data Availability**: Climate data is only available for 1950-1951
2. **Spatial Precision**: The underlying dataset uses grid features; exact coordinate matching may not be available
3. **Country Mapping**: Country names don't automatically map to exact boundaries; coordinates provide better precision
4. **Feature Discovery**: Use "list features" or "features near coordinates" to discover available data points

## Tips for Best Results

1. **Use Coordinates for Precision**: For exact locations, always provide lat/lon
2. **Combine with Time**: Specify time ranges for better results
   - "Temperature at 52.5, 13.4 in January 1950"
3. **Check Available Features**: First query available locations
   - "What locations are available?"
   - "List all features"
4. **Refine Iteratively**: Start broad, then narrow down
   - Start: "Climate in Germany"
   - Refine: "Temperature in Germany at 52.5, 13.4"

## Future Enhancements

Potential improvements:
- Automatic geocoding for city names
- Nearest neighbor search for coordinates
- Bounding box queries for regions
- Country boundary polygon matching
- Distance-based feature filtering

## Example Session

```
User: What's the climate like in Germany?
Agent: I detected you're interested in Germany. For precise location filtering, 
       you can provide coordinates like 'lat: 52.5, lon: 13.4'. 
       [Shows available data for Germany region]

User: Show me temperature at lat: 52.5, lon: 13.4 in 1950
Agent: [Returns temperature data for coordinates 52.5°N, 13.4°E for 1950]
       
User: What about precipitation at the same location?
Agent: [Uses stored coordinates to get precipitation data]
```

## Troubleshooting

**Q: My country name isn't recognized**
A: Use coordinates instead, or contact support to add your country to the list

**Q: Coordinates not working**
A: Verify format - use decimal degrees (e.g., 52.5, not 52°30')

**Q: No data for my location**
A: The dataset only covers 1950-1951 and may not have all global locations

**Q: How to clear location from memory?**
A: Start a new chat session or specify a different location
