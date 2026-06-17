# Multi-Theme Niche Monetized Blog Network

This repository contains five fully responsive, premium, tailwind-designed niche websites optimized for ad placement and lead-generation conversions. Each website features a dynamic landing page, relative internal linking, structured article pages, and standard secondary pages (About, Explore, Privacy, Terms).

---

## 🚀 The Niche Web Network

### 1. **UtilityHQ** (Software Utilities, VPNs, & Cleaner Installs)
* **Goal**: Maximize CPI/CPA conversions for desktop/mobile security tools.
* **Key Content**: Boot speed optimization guides, VPN comparisons (WireGuard), and antivirus Whitelisting.
* **Layout**: Clean, modern, high-contrast dark tech aesthetic.

### 2. **WinDaily** (High-Yield Consumer Sweepstakes & Lead-Gen)
* **Goal**: Capture lead-generation data for retail brand rewards (CPL).
* **Key Content**: Identifying legitimate giveaways, sweepstakes strategies, and budgeting tips.
* **Layout**: High-energy, celebratory aesthetic with gift card and cash reward motifs.

### 3. **CapitalQuest** (Wealth Preservation, Gold IRAs, & Crypto Yields)
* **Goal**: Lead generation for high-payout finance accounts and wealth advisories.
* **Key Content**: Gold IRA tax planning, Ethereum/USDC staking guides, and elite investment habits.
* **Layout**: Luxurious dark green and gold financial theme.

### 4. **BetPlayHub** (Sports Betting & Gaming Strategy)
* **Goal**: iGaming registrations and sportsbook affiliate conversions.
* **Key Content**: Sports betting margin math, casual vs. pro psychology, and security checks.
* **Layout**: Dynamic sports dashboard design.

### 5. **ViralBuzz** (Pop Culture, Listicles, & High-CTR Arbitrage)
* **Goal**: High-CTR display ad arbitrage.
* **Key Content**: Secret travel destinations, coffee alternatives (Matcha), and budget smartphone accessories.
* **Layout**: Highly visual, engaging grid layout.

---

## 📁 Directory Structure

```
.
├── BetPlayHub/            # iGaming/Sports Betting blog files
├── CapitalQuest/          # Wealth & Finance blog files
├── UtilityHQ/             # Software Utility blog files
├── ViralBuzz/             # Pop Culture & Listicles blog files
├── WinDaily/              # Sweepstakes & Giveaway blog files
│   ├── index.html         # Landing page template
│   ├── about.html         # About page
│   ├── privacy.html       # Privacy Policy page
│   ├── terms.html         # Terms of Service page
│   ├── explore.html       # Article search and grid page
│   ├── articles/          # Generated articles (slugified .html)
│   └── images/            # Site-specific local PNG assets
│
├── generate_sites.py      # Core site generation & injection script
├── deploy.sh              # Automatic GitHub deployment assistant
├── README.md              # Project documentation
└── .gitignore             # Configured git ignore files
```

---

## 🛠️ Site Regeneration & Expansion

To add new articles or edit existing content, update the `ARTICLES_DATA` dictionary inside `generate_sites.py` and run the script:

```bash
python3 generate_sites.py
```

The generation script will automatically:
1. Verify that all articles meet the required **500–600 word constraint**.
2. Format the article body paragraphs with custom CSS classes, subheadings, and sponsored banner elements.
3. Generate the individual `.html` article files in each site's `articles/` directory.
4. Update the card components on each homepage (`index.html`) with the latest headlines, descriptions, and local image paths.
5. Create/update the secondary pages (`about.html`, `privacy.html`, `terms.html`, `explore.html`) ensuring styling and link consistency.

---

## 📦 Deployment to GitHub Pages

To deploy the network, push the code to your GitHub repository:

```bash
./deploy.sh
```

*(Note: You will be prompted for your GitHub username and Personal Access Token (PAT) or credentials to complete the push.)*

Once pushed:
1. Go to your repository settings page: `https://github.com/<username>/<repo>/settings/pages`
2. Under **Build and deployment**, set the Source to **Deploy from a branch**.
3. Choose the `main` branch and the `/` (root) folder, and click **Save**.
4. The sites will be live at: `https://<username>.github.io/<repo>/<SiteName>/` (e.g., `https://<username>.github.io/<repo>/UtilityHQ/`).
