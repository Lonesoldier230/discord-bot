import disnake
from modules.general import file_open,color

def embeder(ctx,cat:str = "all",number:int = 0):
    shop_items = file_open("./storage/shop_items.json")
    embed = disnake.Embed(title="Shop", color=color())
    id = ctx.author.id
    num1 = 0+10*number
    num2 = 10+10*number
    if num2 >= len(list(shop_items[cat].keys())):
        num2 = len(list(shop_items[cat].keys()))
            
    for i in range(num1,num2):
        item_name = list(shop_items[cat].keys())[i]
        stock_no = shop_items[cat][i]["stock_no"]
        price = shop_items[cat][i]["price"]
        description = shop_items[cat][i]["description"]
        emoji = shop_items[cat][i]["emoji"]
                
        embed.add_field(name=f"{emoji} {item_name}({stock_no}):{price}", value=description, inline=True)
    embed.set_footer(text=f"#{id}")
    
    return embed