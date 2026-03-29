# Anki Card Generator

LLM prompts and a post-processing script for generating Anki flashcards for language learning.

## Files

| File | Description |
|------|-------------|
| `german_tutor_prompt.txt` | Gemini prompt for German (A1→A2): translation, grammar correction, and Anki card generation |
| `english_tutor_prompt.txt` | Gemini prompt for English: correction, usage feedback, and Anki card generation |
| `process_anki.py` | Post-processing script that converts `{{word}}` markers into correctly-counted underscores |

## How It Works

1. **Paste a prompt** into a Gemini gem as the system instruction.
2. **Send words** separated by semicolons (e.g., `dog; cat; to run`) — the model generates Anki cards.
3. **Copy the output** into a `.tsv` file.
4. **Run the script** to replace `{{word}}` markers with underscores:
   ```bash
   python process_anki.py cards.tsv
   ```
   This produces `cards_processed.tsv` with correct underscore counts.
5. **Import** `cards_processed.tsv` into Anki (tab-delimited, HTML enabled).

## Why `{{markers}}` Instead of Direct Underscores?

LLMs operate on tokens, not characters - they consistently miscount letters. The `{{word}}` approach lets the model output the actual word, and the Python script replaces it with the exact number of underscores.

## Script Usage

```bash
# Basic: input.tsv → input_processed.tsv
python process_anki.py input.tsv

# Custom output path
python process_anki.py input.tsv output.tsv

# Pipe from stdin
echo 'front {{Wort}} here	back' | python process_anki.py -

# Copy to clipboard (requires xclip)
python process_anki.py input.tsv --clipboard
```

The script also validates that each line has exactly one tab separator and warns about any issues.

## Card Types

### German
- **Word cards** — English word on front, German cloze sentence; full word info, IPA, antonym on back
- **Sentence cards** — German sentence on front, English translation on back

### English
- **Word/phrase cards** - meaning + cloze sentence on front; IPA, Russian translation, common mistake, collocations, synonyms, antonyms, register on back
- **Phrasal verb cards** - sentence cloze on front with meaning hint; separability info, common mistakes, collocations on back
