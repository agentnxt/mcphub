import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { mapsPost, mapsGet, buildStaticUrl } from "../api.js";

export function registerAdvancedTools(server: McpServer) {
  // Maps Embed API — builds an iframe-embeddable URL
  server.tool(
    "embed_map",
    "Build a Google Maps Embed API URL for embedding an interactive map in a web page (iframe src)",
    {
      mode: z
        .enum(["place", "view", "directions", "streetview", "search"])
        .describe("Embed mode: place (single location), view (center+zoom), directions, streetview, or search"),
      q: z.string().optional().describe("Query (required for place, search modes). e.g. 'Eiffel Tower' or 'lat,lng'"),
      center: z.string().optional().describe("Center for 'view' mode as 'lat,lng'"),
      zoom: z.number().optional().describe("Zoom level for view mode (0-21)"),
      origin: z.string().optional().describe("Origin for directions mode"),
      destination: z.string().optional().describe("Destination for directions mode"),
      waypoints: z.string().optional().describe("Pipe-separated waypoints for directions mode"),
      mode_directions: z
        .enum(["driving", "walking", "bicycling", "transit", "flying"])
        .optional()
        .describe("Travel mode for directions"),
      location: z.string().optional().describe("Location for streetview mode as 'lat,lng'"),
      pano: z.string().optional().describe("Panorama ID for streetview mode"),
      heading: z.number().optional().describe("Streetview heading (0-360)"),
      pitch: z.number().optional().describe("Streetview pitch (-90 to 90)"),
      fov: z.number().optional().describe("Streetview FOV (10-100)"),
    },
    async (args) => {
      const params: Record<string, string | number | boolean | undefined> = {
        q: args.q,
        center: args.center,
        zoom: args.zoom,
        origin: args.origin,
        destination: args.destination,
        waypoints: args.waypoints,
        mode: args.mode_directions,
        location: args.location,
        pano: args.pano,
        heading: args.heading,
        pitch: args.pitch,
        fov: args.fov,
      };
      const url = buildStaticUrl(`https://www.google.com/maps/embed/v1/${args.mode}`, params);
      return {
        content: [
          {
            type: "text",
            text: `Embed URL (use in iframe src):\n${url}\n\nExample iframe:\n<iframe width="600" height="450" style="border:0" loading="lazy" allowfullscreen src="${url}"></iframe>`,
          },
        ],
      };
    }
  );

  // Map Tiles API — create session
  server.tool(
    "create_map_tile_session",
    "Create a Map Tiles API session token. Required before fetching 2D/3D/street view tiles. Returns a session token and expiry.",
    {
      mapType: z
        .enum(["roadmap", "satellite", "terrain", "streetview"])
        .describe("Type of map tiles"),
      language: z.string().optional().default("en-US").describe("Language code"),
      region: z.string().optional().default("US").describe("Region code"),
      imageFormat: z.enum(["png", "jpeg"]).optional(),
      scale: z.enum(["scaleFactor1x", "scaleFactor2x", "scaleFactor4x"]).optional(),
      highDpi: z.boolean().optional(),
      layerTypes: z
        .array(z.enum(["layerRoadmap", "layerStreetview", "layerTraffic"]))
        .optional()
        .describe("Overlay layers"),
    },
    async (args) => {
      const data = await mapsPost("https://tile.googleapis.com/v1/createSession", {
        mapType: args.mapType,
        language: args.language,
        region: args.region,
        imageFormat: args.imageFormat,
        scale: args.scale,
        highDpi: args.highDpi,
        layerTypes: args.layerTypes,
      });
      return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
    }
  );

  server.tool(
    "get_map_tile_url",
    "Build a Map Tiles API tile URL for a specific z/x/y coordinate. Requires a session token from create_map_tile_session.",
    {
      session: z.string().describe("Session token from create_map_tile_session"),
      z: z.number().describe("Zoom level (0-22)"),
      x: z.number().describe("Tile X coordinate"),
      y: z.number().describe("Tile Y coordinate"),
    },
    async ({ session, z, x, y }) => {
      const url = buildStaticUrl(`https://tile.googleapis.com/v1/2dtiles/${z}/${x}/${y}`, { session });
      return { content: [{ type: "text", text: `Tile URL:\n${url}` }] };
    }
  );

  // Aerial View API
  server.tool(
    "lookup_aerial_view",
    "Look up an existing aerial view cinematic video for an address. Returns video URLs if one exists.",
    {
      address: z.string().describe("The address to look up an aerial view for"),
    },
    async ({ address }) => {
      const data = await mapsGet("https://aerialview.googleapis.com/v1/videos:lookupVideo", { address });
      return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
    }
  );

  server.tool(
    "render_aerial_view",
    "Request a new aerial view cinematic video be rendered for an address. First call may return PROCESSING; call lookup_aerial_view afterwards.",
    {
      address: z.string().describe("The address to render an aerial view for"),
    },
    async ({ address }) => {
      const data = await mapsPost("https://aerialview.googleapis.com/v1/videos:renderVideo", { address });
      return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
    }
  );

  // Places Aggregate API (Area Insights)
  server.tool(
    "compute_area_insights",
    "Compute aggregate insights about places in a given area. Returns counts of places matching filters.",
    {
      insights: z
        .array(z.enum(["INSIGHT_COUNT", "INSIGHT_PLACES"]))
        .describe("Types of insights to compute"),
      filter: z.object({
        locationFilter: z.object({
          circle: z
            .object({
              latLng: z.object({ latitude: z.number(), longitude: z.number() }),
              radius: z.number().describe("Radius in meters"),
            })
            .optional(),
          region: z.object({ place: z.string() }).optional().describe("Region by place ID (e.g. 'places/ChIJ...')"),
        }),
        typeFilter: z
          .object({
            includedTypes: z.array(z.string()).optional().describe("Place types to include"),
            excludedTypes: z.array(z.string()).optional(),
            includedPrimaryTypes: z.array(z.string()).optional(),
            excludedPrimaryTypes: z.array(z.string()).optional(),
          })
          .optional(),
        operatingStatus: z
          .array(
            z.enum(["OPERATING_STATUS_OPERATIONAL", "OPERATING_STATUS_PERMANENTLY_CLOSED", "OPERATING_STATUS_TEMPORARILY_CLOSED"])
          )
          .optional(),
        priceLevels: z
          .array(
            z.enum(["PRICE_LEVEL_FREE", "PRICE_LEVEL_INEXPENSIVE", "PRICE_LEVEL_MODERATE", "PRICE_LEVEL_EXPENSIVE", "PRICE_LEVEL_VERY_EXPENSIVE"])
          )
          .optional(),
        ratingFilter: z
          .object({
            minRating: z.number().optional(),
            maxRating: z.number().optional(),
          })
          .optional(),
      }),
    },
    async ({ insights, filter }) => {
      const data = await mapsPost("https://areainsights.googleapis.com/v1:computeInsights", {
        insights,
        filter,
      });
      return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
    }
  );
}
