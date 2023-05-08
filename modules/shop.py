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
        stock_no = shop_items[cat][item_name]["stock_no"]
        price = shop_items[cat][item_name]["price"]
        description = shop_items[cat][item_name]["description"]
        emoji = shop_items[cat][item_name]["emoji"]
                
        embed.add_field(name=f"{emoji} {item_name}({stock_no}):{price}", value=description, inline=False)
    embed.set_footer(text=f"#{id}")
    
    return embed


class shop_embed:
    def __init__(self):
        self.number = 0

    def add_number(self, num: int = 1):
        self.a += num
        return self.number

    def sub_number(self, num: int = 1):
        self.a -= num
        return self.number

    def set_num(self, num: int = 0):
        self.a = 0
        return self.number
