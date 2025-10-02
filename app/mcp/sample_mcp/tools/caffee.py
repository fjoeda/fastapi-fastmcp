from fastmcp import FastMCP, Context
from fastmcp.server.elicitation import (
    CancelledElicitation,
    AcceptedElicitation
)

def register_tools(mcp: FastMCP):
    @mcp.tool(name="member registration", description="Register a new member")
    async def member_registration(ctx: Context) -> str:
        """
        Introduces yourself with a greeting message.
        """

        name = await ctx.elicit("May I know your name?", response_type=str)
        if name.action != "accept":
            return "Introduction cancelled. No worries!"

        phone_number = await ctx.elicit(f"Hello {name.value}! Could you please provide your phone number?", response_type=str)
        if phone_number.action != "accept":
            return "Introduction cancelled. No worries!"
        
        return f"Hello {name.value}! Your phone number {phone_number.value} has been recorded. Nice to meet you!"
    
    @mcp.tool(name="order food", description="Order food from the menu")
    async def order_food(ctx: Context) -> str:
        """
        Order food from the menu.
        """

        menu = ["Pizza", "Burger", "Sushi", "Pasta", "Salad"]
        menu_str = "\n".join(f"{idx + 1}. {item}" for idx, item in enumerate(menu))
        choice = await ctx.elicit(f"Here is the menu:\n{menu_str}\nPlease select an item by number:")
        if choice.action != "accept":
            return "Order cancelled. No worries!"
        
        try:
            choice_idx = int(choice.value) - 1
            if choice_idx < 0 or choice_idx >= len(menu):
                return "Invalid choice. Order cancelled."
            selected_item = menu[choice_idx]
        except ValueError:
            return "Invalid input. Order cancelled."
        
        quantity = await ctx.elicit(f"How many {selected_item}s would you like to order?")
        if quantity.action != "accept":
            return "Order cancelled. No worries!"
        
        try:
            quantity_num = int(quantity.value)
            if quantity_num <= 0:
                return "Quantity must be positive. Order cancelled."
        except ValueError:
            return "Invalid input. Order cancelled."
        
        return f"Your order for {quantity_num} {selected_item}(s) has been placed successfully!"

        