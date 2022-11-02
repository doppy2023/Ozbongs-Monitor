import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import json
import time
import datetime

with open('settings.json', 'r') as f:
    settings = json.load(f)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

lastPosted = dict()

def main():

    for (idx, link) in enumerate(settings['links']):

        posted = False

        today = datetime.datetime.now().strftime("%Y-%m-%d")
        print(f'Opening link {idx+1} of {len(settings["links"])}')
        
        try:
            response = requests.get(link, headers= headers)
        except:
            print('Error opening link')
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('h1', {'class': 'fn title'}).text
        price = soup.find('span', {'class': 'price product-price'}).text
        image = soup.find('div', class_= "product-photo").find('img')['src']

        if "https:" not in image:
            image = f'https:{image}'

        if soup.find("span", class_= "coming-soon-label"):
            print('Coming Soon detected not posting to discord.')
            availability = soup.find('span', class_= 'coming-soon-label').text.strip().lower()
            time.sleep(10)
            print('Continuing...\n')
            continue
        
        elif soup.find('span', class_= 'stock-level product-in-stock'):
            availability = soup.find('span', class_= 'stock-level product-in-stock').text.strip().lower()
            posted = True

        if "in stock" in availability:

            availability = "In Stock"

            if lastPosted.get(link, None):
                if lastPosted[link] == today:
                    print()
                    print('Already posted today, not posting again. until tomorrow')
                    time.sleep(20)
                    continue
                else:
                    lastPosted[link] = today
                    print('Available! posting to discord')
                    webhook = DiscordWebhook(url=settings['discordWebhookUrl'], content= settings['discordUserId'])
                    embed = DiscordEmbed(title=title, color=0x00FF00)
                    embed.set_url(url= link)
                    embed.set_thumbnail(url=image)
                    embed.add_embed_field(name='Price', value=price, inline= False)
                    embed.add_embed_field(name='Availability', value=availability, inline= False)
                    embed.add_embed_field(name= 'Link', value=f'[Click Here]({link})', inline= False)
                    embed.set_footer(text='Ozbongs Monitor', icon_url='https://i.imgur.com/8K1ZiKA.png')
                    embed.set_author(name='Ozbongs Monitor', url=link, icon_url='https://i.imgur.com/8K1ZiKA.png')
                    embed.set_timestamp()
                    webhook.add_embed(embed)
                    response = webhook.execute()
                    print('Posted to discord')
            else:
                lastPosted[link] = today
                print('Available! posting to discord')
                webhook = DiscordWebhook(url=settings['discordWebhookUrl'], content= settings['discordUserId'])
                embed = DiscordEmbed(title=title, color=0x00FF00)
                embed.set_url(url= link)
                embed.set_thumbnail(url=image)
                embed.add_embed_field(name='Price', value=price, inline= False)
                embed.add_embed_field(name='Availability', value=availability, inline= False)
                embed.add_embed_field(name= 'Link', value=f'[Click Here]({link})', inline= False)
                embed.set_footer(text='Ozbongs Monitor', icon_url='https://i.imgur.com/8K1ZiKA.png')
                embed.set_author(name='Ozbongs Monitor', url=link, icon_url='https://i.imgur.com/8K1ZiKA.png')
                embed.set_timestamp()
                webhook.add_embed(embed)
                response = webhook.execute()
                print('Posted to discord')

        #Check if the add to cart button is there

        if not posted:
            
            if soup.find('div', class_= 'add-button-wrapper widget-fingerprint-product-add-button'):
                availability = "In Stock"

            if lastPosted.get(link, None):

                if lastPosted[link] == today:
                    print()
                    print('Already posted today, not posting again. until tomorrow')
                    time.sleep(20)
                    continue
                
                else:
                        lastPosted[link] = today
                        print('Available! posting to discord')
        
                        webhook = DiscordWebhook(url=settings['discordWebhookUrl'], content= settings['discordUserId'])
                        embed = DiscordEmbed(title=title, color=0x00FF00)
                        embed.set_url(url= link)
                        embed.set_thumbnail(url=image)
                        embed.add_embed_field(name='Price', value=price, inline= False)
                        embed.add_embed_field(name='Availability', value=availability, inline= False)
                        embed.add_embed_field(name= 'Link', value=f'[Click Here]({link})', inline= False)
                        embed.set_footer(text='Ozbongs Monitor', icon_url='https://i.imgur.com/8K1ZiKA.png')
                        embed.set_author(name='Ozbongs Monitor', url=link, icon_url='https://i.imgur.com/8K1ZiKA.png')
                        embed.set_timestamp()
                        webhook.add_embed(embed)
                        response = webhook.execute()
                        print('Posted to discord')
            else:
                lastPosted[link] = today
                print('Available! posting to discord')
                webhook = DiscordWebhook(url=settings['discordWebhookUrl'], content= settings['discordUserId'])
                embed = DiscordEmbed(title=title, color=0x00FF00)
                embed.set_url(url= link)
                embed.set_thumbnail(url=image)
                embed.add_embed_field(name='Price', value=price, inline= False)
                embed.add_embed_field(name='Availability', value=availability, inline= False)
                embed.add_embed_field(name= 'Link', value=f'[Click Here]({link})', inline= False)
                embed.set_footer(text='Ozbongs Monitor', icon_url='https://i.imgur.com/8K1ZiKA.png')
                embed.set_author(name='Ozbongs Monitor', url=link, icon_url='https://i.imgur.com/8K1ZiKA.png')
                embed.set_timestamp()
                webhook.add_embed(embed)
                response = webhook.execute()
                print('Posted to discord')

        
        time.sleep(20)



    print('Sleeping for 1 minute')

if __name__ == '__main__':
    while True:
        main()
        time.sleep(60)