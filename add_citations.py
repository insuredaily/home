with open("generate_sites.py", "r", encoding="utf-8") as f:
    code = f.read()

# Define the citations mapping
citations = {
    "speed-up-windows-boot-time": "\\n\\n**References & Citations:**\\n- [PCWorld: Best PC Cleaner and Optimizer Tools](https://www.pcworld.com)\\n- [CNET: Windows Boot Speed Optimization Guides](https://www.cnet.com)",
    
    "harden-windows-safely": "\\n\\n**References & Citations:**\\n- [Tom's Hardware: How to Optimize Windows for Gaming](https://www.tomshardware.com)\\n- [How-To Geek: Antivirus Whitelisting for Gamers](https://www.howtogeek.com)",
    
    "why-tech-pros-use-wireguard": "\\n\\n**References & Citations:**\\n- [WireGuard Official Protocol Specifications](https://www.wireguard.com)\\n- [NordVPN: WireGuard vs OpenVPN Performance Comparison](https://nordvpn.com)",
    
    "spot-real-giveaways": "\\n\\n**References & Citations:**\\n- [Federal Trade Commission (FTC): Avoiding Sweepstakes Scams](https://www.consumer.ftc.gov)\\n- [The Balance: How to Identify Legitimate Giveaways](https://www.thebalance.com)",
    
    "can-you-win-cash-card": "\\n\\n**References & Citations:**\\n- [AARP: Guide to Entering and Winning Online Sweepstakes](https://www.aarp.org)\\n- [Sweepstakes Today: Legal Requirements for Online Giveaways](https://www.sweepstakes.today)",
    
    "sweepstakes-hunters-save-money": "\\n\\n**References & Citations:**\\n- [The Spruce Crafts: Organising Sweepstakes Entries](https://www.thesprucecrafts.com)\\n- [Consumer Reports: Winning and Saving Strategies](https://www.consumerreports.org)",
    
    "gold-ira-vs-physical-gold": "\\n\\n**References & Citations:**\\n- [Forbes Advisor: Investing in Gold IRAs vs Physical Gold](https://www.forbes.com/advisor)\\n- [Investopedia: Precious Metals Retirement Accounts Guide](https://www.investopedia.com)",
    
    "demystifying-crypto-staking": "\\n\\n**References & Citations:**\\n- [Coinbase Learn: What is Crypto Staking and How Does It Work?](https://www.coinbase.com/learn)\\n- [CoinDesk: Ethereum Staking Yields and Risks](https://www.coindesk.com)",
    
    "wealthy-investors-habits": "\\n\\n**References & Citations:**\\n- [CNBC Make It: Habits of Highly Successful Investors](https://www.cnbc.com/make-it)\\n- [Business Insider: Wealth Management & Asset Allocation](https://www.businessinsider.com)",
    
    "understanding-sports-betting-margins": "\\n\\n**References & Citations:**\\n- [Action Network: How to Calculate Sportsbook Betting Margins](https://www.actionnetwork.com)\\n- [Pinnacle Sports: Understanding Bookmaker Overround and Vigorish](https://www.pinnacle.com)",
    
    "casual-vs-pro-psychology": "\\n\\n**References & Citations:**\\n- [Psychology Today: Cognitive Biases in Sports Gaming](https://www.psychologytoday.com)\\n- [VSiN: Professional Bankroll Management Strategies](https://www.vsin.com)",
    
    "safe-and-secure-online-play": "\\n\\n**References & Citations:**\\n- [TechRadar: Guide to Secure iGaming Platforms and Licensing](https://www.techradar.com)\\n- [Casino.org: Online Gaming Security Checks and Auditing](https://www.casino.org)",
    
    "secret-travel-destinations": "\\n\\n**References & Citations:**\\n- [Lonely Planet: Budget Travel and Off-Peak Destinations](https://www.lonelyplanet.com)\\n- [Travel + Leisure: Hidden Destinations That Cost Less](https://www.travelandleisure.com)",
    
    "why-genz-ditches-coffee-shops": "\\n\\n**References & Citations:**\\n- [Healthline: Health Benefits of Matcha Green Tea vs Coffee](https://www.healthline.com)\\n- [Bon Appétit: Gen Z Cafe Culture and Matcha Trends](https://www.bonappetit.com)",
    
    "best-budget-smartphone-accessories": "\\n\\n**References & Citations:**\\n- [Wirecutter (NYT): Best Budget Phone Accessories](https://www.nytimes.com/wirecutter)\\n- [Android Police: Essential Cheap Mobile Gear and Accessories](https://www.androidpolice.com)"
}

for slug, cit_text in citations.items():
    slug_pat = f'"slug": "{slug}"'
    slug_idx = code.find(slug_pat)
    if slug_idx == -1:
        print(f"Error: Could not find slug {slug}")
        continue
    
    body_key = '"body": """'
    body_idx = code.find(body_key, slug_idx)
    start_body = body_idx + len(body_key)
    end_body = code.find('"""', start_body)
    
    original_body = code[start_body:end_body]
    # Check if already cited
    if "References & Citations:" in original_body:
        print(f"{slug} already cited. Replacing it.")
        # Remove old citations
        cit_start = original_body.find("\n\n**References & Citations:**")
        if cit_start != -1:
            original_body = original_body[:cit_start]
            
    # Append citation
    new_body = original_body.rstrip() + cit_text
    code = code[:start_body] + new_body + code[end_body:]

with open("generate_sites.py", "w", encoding="utf-8") as f:
    f.write(code)

print("generate_sites.py successfully updated with citations!")
