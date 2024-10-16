import os
from dotenv import load_dotenv
import requests
from telegram import Update, ParseMode
from telegram.ext import CallbackContext

load_dotenv()

def fetch_access_token():
    url = "https://oauth2.bitquery.io/oauth2/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': os.getenv('BITQUERY_CLIENT_ID'),
        'client_secret': os.getenv('BITQUERY_CLIENT_SECRET'),
        'scope': 'api'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, headers=headers, data=payload)
    resp_json = response.json()
    
    if 'access_token' in resp_json:
        return resp_json['access_token']
    else:
        print(f"Failed to fetch access token. Error: {resp_json.get('error_description', 'Unknown error')}")
        return None

def fetch_nft_data():
    access_token = fetch_access_token()
    if not access_token:
        print("Failed to obtain access token")
        return None
    
    url = 'https://streaming.bitquery.io/graphql'
    
    graphql_query = """
    query MyQuery {
      EVM(dataset: combined, network: eth) {
        DEXTrades(
          where: {Trade: {Dex: {ProtocolName: {in: "seaport_v1.4"}}}, Transaction: {To: {is: "0x00000000000000adc04c56bf30ac9d3c0aaf14dc"}}}
          orderBy: {descendingByField: "count"}
          limit: {count: 10}
        ) {
          tradeVol: sum(of: Trade_Buy_Amount)
          count
          buyers: count(distinct: Trade_Buy_Buyer)
          seller: count(distinct: Trade_Buy_Seller)
          nfts: count(distinct: Trade_Buy_Ids)
          Trade {
            Buy {
              Currency {
                Name
                ProtocolName
                Symbol
                Fungible
                SmartContract
              }
            }
          }
        }
      }
    }
    """

    headers_graphql = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.post(url, headers=headers_graphql, json={'query': graphql_query})
        response.raise_for_status()

        response_json = response.json()
        print("API Response:", response_json)  # Debug print

        if 'data' in response_json and response_json['data'] is not None:
            if 'EVM' in response_json['data'] and response_json['data']['EVM'] is not None:
                if 'DEXTrades' in response_json['data']['EVM']:
                    return response_json['data']['EVM']['DEXTrades']
                else:
                    print("'DEXTrades' not found in response")
            else:
                print("'EVM' not found in response or is None")
        else:
            print("'data' not found in response or is None")

        if 'errors' in response_json:
            print("Errors in API response:", response_json)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    return None

def escape_markdown(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

def create_table(nft_data):
    table = "*Top 10 Traded NFTs in the Last 30 Days:*\n\n"
    
    for item in nft_data:
        symbol = item['Trade']['Buy']['Currency']['Symbol']
        trades = int(item['count'])
        buyers = int(item['buyers'])
        sellers = int(item['seller'])
        nfts = int(item['nfts'])
        trade_vol = float(item['tradeVol'])
        
        if not symbol:  # If symbol is missing or empty
            smart_contract = item['Trade']['Buy']['Currency']['SmartContract']
            symbol = f"NFT ({smart_contract[:6]}...{smart_contract[-4:]})"
        
        table += f"Symbol: {symbol}\n"
        table += f"Trades: {trades:,}\n"
        table += f"Buyers: {buyers}\n"
        table += f"Sellers: {sellers}\n"
        table += f"NFTs: {nfts}\n"
        table += f"Trade Volume: {trade_vol:,.2f}\n"
        table += "-" * 30 + "\n"
    
    return table

def nft_analysis(update: Update, context: CallbackContext) -> None:
    nft_data = fetch_nft_data()
    if nft_data:
        table = create_table(nft_data)
        update.message.reply_text(table)
    else:
        update.message.reply_text("Failed to fetch NFT data")