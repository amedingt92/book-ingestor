import sys
import os

# Enable importing from the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingest import load_book
from src.structure import split_into_chapters, clean_gutenberg_text
from src.summarizer import summarize_long_text, save_summaries
from tqdm import tqdm
from transformers import pipeline

book = "books/frankenstein.txt"
book_output = "summaries/frankenstein.md"

# Load summarizer pipeline
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

# def refine_summary(text):
#     return text.strip()

# def test_summarizer_with_sample():
#     sample_text = """
#     I am by birth a Genevese, and my family is one of the most
# distinguished of that republic. My ancestors had been for many years
# counsellors and syndics, and my father had filled several public
# situations with honour and reputation. He was respected by all who
# knew him for his integrity and indefatigable attention to public
# business. He passed his younger days perpetually occupied by the
# affairs of his country; a variety of circumstances had prevented his
# marrying early, nor was it until the decline of life that he became a
# husband and the father of a family.

# As the circumstances of his marriage illustrate his character, I cannot
# refrain from relating them. One of his most intimate friends was a
# merchant who, from a flourishing state, fell, through numerous
# mischances, into poverty. This man, whose name was Beaufort, was of a
# proud and unbending disposition and could not bear to live in poverty
# and oblivion in the same country where he had formerly been
# distinguished for his rank and magnificence. Having paid his debts,
# therefore, in the most honourable manner, he retreated with his
# daughter to the town of Lucerne, where he lived unknown and in
# wretchedness. My father loved Beaufort with the truest friendship and
# was deeply grieved by his retreat in these unfortunate circumstances.
# He bitterly deplored the false pride which led his friend to a conduct
# so little worthy of the affection that united them. He lost no time in
# endeavouring to seek him out, with the hope of persuading him to begin
# the world again through his credit and assistance.

# Beaufort had taken effectual measures to conceal himself, and it was ten
# months before my father discovered his abode. Overjoyed at this discovery,
# he hastened to the house, which was situated in a mean street near the
# Reuss. But when he entered, misery and despair alone welcomed him. Beaufort
# had saved but a very small sum of money from the wreck of his fortunes, but
# it was sufficient to provide him with sustenance for some months, and in
# the meantime he hoped to procure some respectable employment in a
# merchant’s house. The interval was, consequently, spent in inaction;
# his grief only became more deep and rankling when he had leisure for
# reflection, and at length it took so fast hold of his mind that at the end
# of three months he lay on a bed of sickness, incapable of any exertion.

# His daughter attended him with the greatest tenderness, but she saw
# with despair that their little fund was rapidly decreasing and that
# there was no other prospect of support. But Caroline Beaufort
# possessed a mind of an uncommon mould, and her courage rose to support
# her in her adversity. She procured plain work; she plaited straw and
# by various means contrived to earn a pittance scarcely sufficient to
# support life.

# Several months passed in this manner. Her father grew worse; her time
# was more entirely occupied in attending him; her means of subsistence
# decreased; and in the tenth month her father died in her arms, leaving
# her an orphan and a beggar. This last blow overcame her, and she knelt
# by Beaufort’s coffin weeping bitterly, when my father entered the
# chamber. He came like a protecting spirit to the poor girl, who
# committed herself to his care; and after the interment of his friend he
# conducted her to Geneva and placed her under the protection of a
# relation. Two years after this event Caroline became his wife.

# There was a considerable difference between the ages of my parents, but
# this circumstance seemed to unite them only closer in bonds of devoted
# affection. There was a sense of justice in my father’s upright mind
# which rendered it necessary that he should approve highly to love
# strongly. Perhaps during former years he had suffered from the
# late-discovered unworthiness of one beloved and so was disposed to set
# a greater value on tried worth. There was a show of gratitude and
# worship in his attachment to my mother, differing wholly from the
# doting fondness of age, for it was inspired by reverence for her
# virtues and a desire to be the means of, in some degree, recompensing
# her for the sorrows she had endured, but which gave inexpressible grace
# to his behaviour to her. Everything was made to yield to her wishes
# and her convenience. He strove to shelter her, as a fair exotic is
# sheltered by the gardener, from every rougher wind and to surround her
# with all that could tend to excite pleasurable emotion in her soft and
# benevolent mind. Her health, and even the tranquillity of her hitherto
# constant spirit, had been shaken by what she had gone through. During
# the two years that had elapsed previous to their marriage my father had
# gradually relinquished all his public functions; and immediately after
# their union they sought the pleasant climate of Italy, and the change
# of scene and interest attendant on a tour through that land of wonders,
# as a restorative for her weakened frame.

# From Italy they visited Germany and France. I, their eldest child, was born
# at Naples, and as an infant accompanied them in their rambles. I remained
# for several years their only child. Much as they were attached to each
# other, they seemed to draw inexhaustible stores of affection from a very
# mine of love to bestow them upon me. My mother’s tender caresses and
# my father’s smile of benevolent pleasure while regarding me are my
# first recollections. I was their plaything and their idol, and something
# better—their child, the innocent and helpless creature bestowed on
# them by Heaven, whom to bring up to good, and whose future lot it was in
# their hands to direct to happiness or misery, according as they fulfilled
# their duties towards me. With this deep consciousness of what they owed
# towards the being to which they had given life, added to the active spirit
# of tenderness that animated both, it may be imagined that while during
# every hour of my infant life I received a lesson of patience, of charity,
# and of self-control, I was so guided by a silken cord that all seemed but
# one train of enjoyment to me.

# For a long time I was their only care. My mother had much desired to have a
# daughter, but I continued their single offspring. When I was about five
# years old, while making an excursion beyond the frontiers of Italy, they
# passed a week on the shores of the Lake of Como. Their benevolent
# disposition often made them enter the cottages of the poor. This, to my
# mother, was more than a duty; it was a necessity, a
# passion—remembering what she had suffered, and how she had been
# relieved—for her to act in her turn the guardian angel to the
# afflicted. During one of their walks a poor cot in the foldings of a vale
# attracted their notice as being singularly disconsolate, while the number
# of half-clothed children gathered about it spoke of penury in its worst
# shape. One day, when my father had gone by himself to Milan, my mother,
# accompanied by me, visited this abode. She found a peasant and his wife,
# hard working, bent down by care and labour, distributing a scanty meal to
# five hungry babes. Among these there was one which attracted my mother far
# above all the rest. She appeared of a different stock. The four others were
# dark-eyed, hardy little vagrants; this child was thin and very fair. Her
# hair was the brightest living gold, and despite the poverty of her
# clothing, seemed to set a crown of distinction on her head. Her brow was
# clear and ample, her blue eyes cloudless, and her lips and the moulding of
# her face so expressive of sensibility and sweetness that none could behold
# her without looking on her as of a distinct species, a being heaven-sent,
# and bearing a celestial stamp in all her features.

# The peasant woman, perceiving that my mother fixed eyes of wonder and
# admiration on this lovely girl, eagerly communicated her history. She was
# not her child, but the daughter of a Milanese nobleman. Her mother was a
# German and had died on giving her birth. The infant had been placed with
# these good people to nurse: they were better off then. They had not been
# long married, and their eldest child was but just born. The father of their
# charge was one of those Italians nursed in the memory of the antique glory
# of Italy—one among the _schiavi ognor frementi,_ who exerted
# himself to obtain the liberty of his country. He became the victim of its
# weakness. Whether he had died or still lingered in the dungeons of Austria
# was not known. His property was confiscated; his child became an orphan and
# a beggar. She continued with her foster parents and bloomed in their rude
# abode, fairer than a garden rose among dark-leaved brambles.

# When my father returned from Milan, he found playing with me in the hall of
# our villa a child fairer than pictured cherub—a creature who seemed
# to shed radiance from her looks and whose form and motions were lighter
# than the chamois of the hills. The apparition was soon explained. With his
# permission my mother prevailed on her rustic guardians to yield their
# charge to her. They were fond of the sweet orphan. Her presence had seemed
# a blessing to them, but it would be unfair to her to keep her in poverty
# and want when Providence afforded her such powerful protection. They
# consulted their village priest, and the result was that Elizabeth Lavenza
# became the inmate of my parents’ house—my more than
# sister—the beautiful and adored companion of all my occupations and
# my pleasures.

# Everyone loved Elizabeth. The passionate and almost reverential
# attachment with which all regarded her became, while I shared it, my
# pride and my delight. On the evening previous to her being brought to
# my home, my mother had said playfully, “I have a pretty present for my
# Victor—tomorrow he shall have it.” And when, on the morrow, she
# presented Elizabeth to me as her promised gift, I, with childish
# seriousness, interpreted her words literally and looked upon Elizabeth
# as mine—mine to protect, love, and cherish. All praises bestowed on
# her I received as made to a possession of my own. We called each other
# familiarly by the name of cousin. No word, no expression could body
# forth the kind of relation in which she stood to me—my more than
# sister, since till death she was to be mine only.
#     """
    
#     summary = summarize_long_text(sample_text)
#     print("\n✅ Summary of Frankenstein Chapter 1:\n")
#     print(summary)
    
# # Run the test
# test_summarizer_with_sample()

if __name__ == "__main__":


    # Load raw book text
    with open(book, "r", encoding="utf-8") as f:
        raw_text = f.read()

    print("📖 Splitting into chapters...")
    clean_text = clean_gutenberg_text(raw_text)
    chapters = split_into_chapters(clean_text)
    print(f"✅ Total chapters detected: {len(chapters)}\n")

    print(f"📚 Previewing first {len(chapters)} chapter titles:")
    for ch in chapters:
        print(f"  - {ch['title']}")


    # print("📚 Previewing first 3 chapter titles:")
    # for i, (title, _) in enumerate(chapters[:3]):
    #     print(f"  - {title}")
    # print()

    # summaries = []

    # for chapter_title, chapter_text in tqdm(chapters, desc="Summarizing Chapters", unit="chapter"):
    #     if len(chapter_text.strip()) > 500:
    #         print(f"🧠 Summarizing {chapter_title}...\n")
    #         print(f"🧾 Length of Chapter Text: {len(chapter_text.strip())} characters\n")

    #         # print("📖 Previewing first 500 characters of chapter:\n")
    #         # print(chapter_text[:500])
    #         # print("\n--- End of Preview ---\n")

    #         try:
    #             summary = summarize_long_text(chapter_text)
    #             # print(f"🔍 Summary of {chapter_title}:\n")
    #             # print(summary[:500] + ("..." if len(summary) > 500 else ""))
    #             summaries.append((chapter_title, summary))
    #         except Exception as e:
    #             print(f"❌ Error summarizing {chapter_title}:", e)
    #     else:
    #         print(f"⚠️ Skipping short chapter: {chapter_title}")

    # print(f"\n💾 Saving all summaries to {book_output}...")
    # save_summaries(summaries, book_output)
    # print("✅ Done.")
