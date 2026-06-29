# roblox-mcp-bridge
MCP bridge that connects Roblox Studio to local AI agents


### Prerequisites
1. Open **Roblox Studio**.
2. Open any project and navigate to the **Assistant** panel.
3. Click the three dots (**...**), select **Manage MCP Servers**, and ensure the option is enabled.
4. Locate and copy the absolute path to your local `mcp.bat` file.

### Running from Source
1. Clone this repository to your local machine.
2. Edit `config.json` and paste your absolute path into the `ROBLOX_MCP_PATH` variable.
3. Double-click `run.bat` to automatically build the virtual environment, install dependencies, and launch the server.

