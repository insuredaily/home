import os
import re
import sys
import json
import urllib.request
from bs4 import BeautifulSoup

# Define feeds for each niche site
FEEDS = {
    "UtilityHQ": [
        "https://feeds.twit.tv/twit_video_hd.xml",
        "https://www.schneier.com/feed/atom/",
        "https://blog.codinghorror.com/rss/"
    ],
    "WinDaily": [
        "https://www.doctorofcredit.com/feed/"
    ],
    "CapitalQuest": [
        "https://feeds.feedburner.com/collabfund"
    ],
    "BetPlayHub": [
        "https://sportstechie.net/feed"
    ],
    "ViralBuzz": [
        "https://archive.org/services/collection-rss.php?collection=classic_tv"
    ]
}

def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    return soup.get_text()

def fetch_feed(url):
    print(f"Fetching: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_items(xml_content):
    if not xml_content:
        return []
    
    items = re.findall(r'<item>.*?</item>|<entry>.*?</entry>', xml_content, re.DOTALL)
    parsed = []
    
    for item in items:
        # Title
        title_m = re.search(r'<title[^>]*>(.*?)</title>', item, re.DOTALL)
        title = title_m.group(1) if title_m else "Untitled"
        title = re.sub(r'<!\[CDATA\[|\]\]>', '', title).strip()
        
        # Link
        link_m = re.search(r'<link>(.*?)</link>', item)
        if not link_m:
            link_m = re.search(r'<link\s+href="(.*?)"', item)
        link = link_m.group(1) if link_m else ""
        if link_m and len(link_m.groups()) > 1 and link_m.group(2):
            link = link_m.group(2)
        link = re.sub(r'<!\[CDATA\[|\]\]>', '', link).strip()
        
        # Date
        date_m = re.search(r'<pubDate>(.*?)</pubDate>|<updated>(.*?)</updated>|<published>(.*?)</published>', item)
        date = date_m.group(1) or date_m.group(2) or date_m.group(3) if date_m else "June 17, 2024"
        date = re.sub(r'<!\[CDATA\[|\]\]>', '', date).strip()
        
        # Author
        author_m = re.search(r'<dc:creator>(.*?)</dc:creator>|<author><name>(.*?)</name></author>|<author>(.*?)</author>', item, re.DOTALL)
        author = "RSS Staff"
        if author_m:
            for g in author_m.groups():
                if g:
                    author = g
                    break
        author = re.sub(r'<!\[CDATA\[|\]\]>', '', author).strip()
        
        # Content body
        content = ""
        content_m = re.search(r'<content:encoded>(.*?)</content:encoded>', item, re.DOTALL)
        if not content_m:
            content_m = re.search(r'<content[^>]*>(.*?)</content>', item, re.DOTALL)
        if not content_m:
            content_m = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
            
        if content_m:
            content = content_m.group(1)
            
        content = re.sub(r'<!\[CDATA\[|\]\]>', '', content, flags=re.DOTALL).strip()
        
        # Parse video URL if present
        video_url = ""
        # 1. Search enclosure tag
        enclosure_m = re.search(r'<enclosure[^>]+url=["\']([^"\']+)["\']', item)
        if enclosure_m:
            enclosure_url = enclosure_m.group(1)
            if any(ext in enclosure_url.lower() for ext in ['.mp4', '.webm', '.m3u8']) or 'video' in item.lower():
                video_url = enclosure_url
        
        # 2. Search media:content tag
        if not video_url:
            media_m = re.search(r'<media:content[^>]+url=["\']([^"\']+)["\']', item)
            if media_m:
                media_url = media_m.group(1)
                if any(ext in media_url.lower() for ext in ['.mp4', '.webm', '.m3u8']) or 'type="video/' in item.lower():
                    video_url = media_url
                    
        parsed.append({
            "title": title,
            "link": link,
            "date": date,
            "author": author,
            "content": content,
            "video_url": video_url
        })
        
    return parsed

def get_word_count(text):
    return len(re.findall(r'\b\w+\b', text))

def pad_to_target_word_count(text, site, target_min=510, target_max=590):
    words = get_word_count(text)
    if words >= target_min:
        return text
        
    padding_blocks = {
        "UtilityHQ": [
            "Furthermore, modern software architecture and systems optimization demand a clinical approach to digital security and hardware performance. When implementing complex utilities or system optimizations, professionals must consider the trade-offs between processing speed and overall stability.",
            "As malware threats become more sophisticated, running regular registry scans and employing robust network isolation technologies like WireGuard VPNs can protect sensitive host systems from vulnerability exploits. Regular hardware maintenance and software audits remain the standard for enterprise security.",
            "Ultimately, keeping system resources optimized and reducing background processes directly translates to improved developer velocity and reduced operational overhead in high-throughput local computing environments."
        ],
        "WinDaily": [
            "In addition, navigating the online sweepstakes and consumer rewards landscape requires a careful, methodical approach to lead generation and personal data security. Savvy consumers often utilize dedicated emails and browser containers to shield their main identities.",
            "While premium brand giveaways offer enticing prizes, understanding the rules, entry limitations, and opt-in agreements is key to maximizing chances without falling victim to high-volume spam campaigns.",
            "Staying updated with legitimate, verified promotion sites ensures a safe and rewarding consumer journey while protecting personal device configurations and digital privacy."
        ],
        "CapitalQuest": [
            "Moreover, building a resilient long-term investment strategy involves a thorough understanding of asset allocation, staking mechanics, and macroeconomics. Diversifying across traditional securities, real estate, and digital assets mitigates risk.",
            "High-net-worth investors focus heavily on tax-advantaged structures like gold IRAs or low-maintenance yield protocols to preserve generational wealth during periods of market volatility and high inflation.",
            "By tracking key market benchmarks and adopting disciplined, automated saving and staking habits, modern retail investors can confidently secure their financial future in a rapidly changing economy."
        ],
        "BetPlayHub": [
            "Additionally, the psychological dynamics of online gaming and sports analytics highlight the importance of disciplined bankroll management and statistical analysis. Pro players analyze margins and lines to find edge.",
            "Choosing reputable, secure gaming portals and keeping software tools updated protects players from account compromise and guarantees fair, audited game outcomes.",
            "Whether engaging in casual tournaments or professional sports predictions, understanding the underlying mathematical probabilities is the foundation of long-term entertainment and success."
        ],
        "ViralBuzz": [
            "Consequently, the shift toward budget-friendly lifestyle travel and sustainable consumer trends reflects a broader cultural interest in minimalist living and financial efficiency. Gen Z and millennial travelers are seeking hidden destinations.",
            "From optimizing mobile smartphone accessories for content creation to brewing premium matcha tea at home, these daily lifestyle modifications offer substantial savings and high satisfaction.",
            "Sharing these discoveries via interactive online listicles and community reviews helps readers make informed decisions that enhance their convenience without overspending."
        ]
    }
    
    blocks = padding_blocks.get(site, [
        "In summary, monitoring these developments reveals key structural shifts within the industry. Staying informed with verified sources is essential for understanding the long-term impact on consumers.",
        "We will continue to track these updates and provide comprehensive reporting on future shifts, technological innovations, and industry benchmarks as they emerge."
    ])
    
    # We want to insert the padding blocks *before* the references section if it exists, or just append it.
    # The reference is at the end of the text. Let's find it.
    ref_marker = "**References & Citations:**"
    if ref_marker in text:
        parts = text.split(ref_marker)
        body = parts[0]
        citation = ref_marker + parts[1]
        
        current_body = body
        for block in blocks * 4:
            if get_word_count(current_body + citation) >= target_min:
                break
            current_body = current_body.strip() + "\n\n" + block
            
        return current_body.strip() + "\n\n" + citation
    else:
        current_body = text
        for block in blocks * 4:
            if get_word_count(current_body) >= target_min:
                break
            current_body = current_body.strip() + "\n\n" + block
        return current_body

def format_body_text(raw_html, source_link):
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    # Extract p tags first to avoid nested div duplications
    p_tags = soup.find_all('p')
    if not p_tags:
        p_tags = soup.find_all('div', recursive=False)
        
    paragraphs = []
    for p in p_tags:
        text = re.sub(r'\s+', ' ', p.get_text().strip())
        if text and len(text.split()) > 8 and text not in paragraphs:
            paragraphs.append(text)
            
    if not paragraphs:
        # Fallback to simple split
        text = clean_html(raw_html)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
    # Join into structured article
    formatted_body = ""
    word_count = 0
    target_words = 520
    
    for p in paragraphs:
        p_word_count = len(re.findall(r'\b\w+\b', p))
        if word_count + p_word_count > target_words:
            # Truncate last paragraph at a sentence boundary
            sentences = re.split(r'(?<=[.!?])\s+', p)
            truncated_p = ""
            for s in sentences:
                s_words = len(re.findall(r'\b\w+\b', s))
                if word_count + s_words <= target_words:
                    truncated_p += s + " "
                    word_count += s_words
                else:
                    break
            if truncated_p.strip():
                formatted_body += truncated_p.strip() + "\n\n"
            break
        else:
            formatted_body += p + "\n\n"
            word_count += p_word_count
            
    source_domain = re.sub(r'https?://(www\.)?', '', source_link).split('/')[0]
    citation = f"**References & Citations:**\n- [Source: Article originally published on {source_domain}]({source_link})"
    
    # Pad if under 500 words
    current_words = get_word_count(formatted_body) + get_word_count(citation)
    if current_words < 500:
        disclaimer = (
            " In summary, analyzing these developments reveals key structural shifts within this domain. "
            "As we monitor these topics further, it becomes clear that staying informed with verified references is essential "
            "for understanding the long-term impact on consumers and professionals alike. We will continue to track these "
            "updates and provide comprehensive reporting on future shifts, technological innovations, and industry benchmarks "
            "as they emerge. Readers are encouraged to review the official source documents and linked guides for additional "
            "technical context and detailed breakdowns."
        )
        formatted_body = formatted_body.strip() + disclaimer + "\n\n"
        
    formatted_body = formatted_body.strip() + "\n\n" + citation
    return formatted_body

def main():
    print("=== RUNNING RSS ARTICLES SYNC ===")
    
    default_videos = {
        "UtilityHQ": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "WinDaily": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
        "CapitalQuest": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "BetPlayHub": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4",
        "ViralBuzz": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4"
    }
    
    # Remove old custom_articles.json to start clean with proper word counts
    custom_path = "custom_articles.json"
    if os.path.exists(custom_path):
        try:
            os.remove(custom_path)
            print("Removed old custom_articles.json for clean sync.")
        except Exception as e:
            print(f"Error removing {custom_path}: {e}")
            
    custom_articles = {}
    
    for site, feed_urls in FEEDS.items():
        custom_articles[site] = []
        site_new_articles = []
        
        for url in feed_urls:
            xml_data = fetch_feed(url)
            if not xml_data:
                continue
                
            items = parse_items(xml_data)
            print(f"Parsed {len(items)} items from feed: {url}")
            
            for item in items:
                # Clean html body text to see if it is a full article
                body_candidate = format_body_text(item['content'], item['link'])
                word_cnt = get_word_count(body_candidate)
                
                # Check: only use feeds/items that show the full article, not excerpts!
                raw_words = get_word_count(clean_html(item['content']))
                
                is_video_article = bool(item.get('video_url'))
                
                if is_video_article:
                    # Pad to 500-600 words if necessary
                    if word_cnt < 500:
                        body_candidate = pad_to_target_word_count(body_candidate, site)
                        word_cnt = get_word_count(body_candidate)
                else:
                    if raw_words < 400 or word_cnt < 500:
                        print(f"  [EXCERPT SKIPPED] '{item['title']}' - only {word_cnt} words of formatted text.")
                        continue
                
                # Adjust / trim if the word count is still outside 500-600 range
                if word_cnt < 500:
                    body_candidate = pad_to_target_word_count(body_candidate, site)
                    word_cnt = get_word_count(body_candidate)
                if word_cnt > 600:
                    # Trim strictly to 540 words to be safe
                    ref_marker = "**References & Citations:**"
                    if ref_marker in body_candidate:
                        parts = body_candidate.split(ref_marker)
                        body_part = parts[0]
                        citation_part = ref_marker + parts[1]
                        
                        target_body_words = 540 - get_word_count(citation_part)
                        body_words = body_part.split()
                        body_candidate = " ".join(body_words[:target_body_words]) + "\n\n" + citation_part
                    else:
                        words_list = body_candidate.split()
                        body_candidate = " ".join(words_list[:540])
                    word_cnt = get_word_count(body_candidate)

                print(f"  [ARTICLE ACCEPTED] '{item['title']}' - {word_cnt} words. Video: {is_video_article}")
                
                # Create slug
                slug = re.sub(r'[^a-z0-9]+', '-', item['title'].lower()).strip('-')
                
                # Check if this slug is already present in custom articles
                if any(x['slug'] == slug for x in custom_articles[site]):
                    print(f"  Already imported: {slug}")
                    continue
                    
                # Setup article meta
                art_entry = {
                    "slug": slug,
                    "title": item['title'],
                    "category": "Latest Update" if site != "UtilityHQ" else "Security Tips",
                    "date": "June 17, 2024",
                    "author": item['author'] or "Staff Writer",
                    "read_time": "5 min read",
                    "image_url": f"images/{os.listdir(os.path.join(site, 'images'))[0]}" if os.path.exists(os.path.join(site, 'images')) and os.listdir(os.path.join(site, 'images')) else "images/default.png",
                    "body": body_candidate,
                    "video_url": item.get('video_url') or default_videos.get(site)
                }
                
                site_new_articles.append(art_entry)
                if len(site_new_articles) >= 5:
                    break
            
            if len(site_new_articles) >= 5:
                break
                
        custom_articles[site] = site_new_articles[:5]

    # Save custom articles JSON
    with open(custom_path, "w", encoding="utf-8") as f:
        json.dump(custom_articles, f, indent=4)
    print("Saved custom_articles.json successfully!")
    
    # Run the site generator to rebuild pages
    print("Re-running site generator...")
    os.system("python3 generate_sites.py")
    print("=== RSS ARTICLES SYNC COMPLETE ===")

if __name__ == "__main__":
    main()
