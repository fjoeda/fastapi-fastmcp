from fastmcp import FastMCP


def register_tools(mcp: FastMCP):
    @mcp.tool(name="get_habitat", description="Get habitat information for an animal")
    def get_habitat(animal: str) -> str:
        """
        Returns the habitat of the given animal.
        """
        habitats = {
            "lion": "Savannah",
            "penguin": "Antarctica",
            "eagle": "Mountains and forests",
            "dolphin": "Oceans and seas",
            "kangaroo": "Australian outback",
        }
        return habitats.get(animal.lower(), "Unknown habitat")
    
    @mcp.tool(name="is_endangered", description="Check if an animal is endangered")
    def is_endangered(animal: str) -> bool:
        """
        Returns True if the animal is endangered, False otherwise.
        """
        endangered_animals = {"tiger", "elephant", "rhino", "panda", "gorilla"}
        return animal.lower() in endangered_animals
