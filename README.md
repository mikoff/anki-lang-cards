# 🃏 Anki Card Generator

Gemini prompts + a script to generate Anki flashcards for language learning.

## 🚀 Usage

1. Use `german_tutor_prompt.txt` or `english_tutor_prompt.txt` as a Gemini system prompt.
2. Send words separated by semicolons: `dog; cat; to run`
3. Save the output as a `.tsv` file.
4. Run the script to fix cloze underscores:
   ```bash
   python process_anki.py cards.tsv
   # → cards_processed.tsv
   ```
5. Import `cards_processed.tsv` into Anki (tab-delimited, HTML enabled).

## 🤔 Why `{{markers}}`?

LLMs miscount characters. The script replaces `{{word}}` with the exact number of underscores.

## ⚙️ Script options

```bash
python process_anki.py input.tsv            # → input_processed.tsv
python process_anki.py input.tsv out.tsv    # custom output
python process_anki.py input.tsv --clipboard  # copy to clipboard
echo '...' | python process_anki.py -       # stdin
```
