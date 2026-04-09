#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { registerGeocodingTools } from "./tools/geocoding.js";
import { registerPlacesTools } from "./tools/places.js";
import { registerRoutingTools } from "./tools/routing.js";
import { registerMapsTools } from "./tools/maps.js";
import { registerLocationTools } from "./tools/location.js";
import { registerEnvironmentTools } from "./tools/environment.js";
import { registerAdvancedTools } from "./tools/advanced.js";

const server = new McpServer({
  name: "google-maps-mcp",
  version: "1.0.0",
});

// Register all tool groups
registerGeocodingTools(server);
registerPlacesTools(server);
registerRoutingTools(server);
registerMapsTools(server);
registerLocationTools(server);
registerEnvironmentTools(server);
registerAdvancedTools(server);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
