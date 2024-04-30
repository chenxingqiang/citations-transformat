import re

def preprocess_citation(citation):
    citation = re.sub(r'\.{2,}', '.', citation)
    citation = re.sub(r'(\d+)\.\s*([A-Z])', r'\1. \2', citation)
    citation = re.sub(r'\(\s*([^)]+)\s*\)\s*\(\s*\1\s*\)', r'(\1)', citation)
    citation = re.sub(r'"\.\s*([^"]+)"\.\s*', r'"\1". ', citation)
    citation = re.sub(r'([A-Z])\s+(\d+)\.', r'\2. \1', citation)
    citation = re.sub(r'(\d+)\.\s*([^A-Z\d\s]+(?:\s+[^A-Z\d\s]+)*),\s*([^,]+),\s*([^.]+)\.', r'\1. \3, \2, \4.', citation)
    citation = re.sub(r'Dis-\s*tribution', 'Distribution', citation)
    return citation

def convert_to_lncs(citation):
    try:
        if '[C]' in citation:
            parts = citation.split('[C]')
            authors = parts[0].split(',')
            authors = [f"{a.split()[-1]} {' '.join(a.split()[:-1])}" for a in authors]
            authors = ', '.join(authors)
            title = parts[1].split('//')[0].strip()
            conference = parts[1].split('//')[1].split('.')[0].strip()
            year = parts[1].split('.')[-2].split()[-1]
            pages = parts[1].split('.')[-2].split(':')[1].strip()
            return f"{authors}. {title}. In: {conference}, pp. {pages} ({year})"
        else:
            parts = citation.split('"')
            if len(parts) < 3:
                parts = citation.split('.')
                if '[J]' in parts[1]:
                    title = parts[1].split('[J]')[0].strip()
                    authors = f'"{parts[0].strip()}"'
                    journal = parts[1].split('[J]')[1].strip()
                    year = parts[-1].strip()
                    return f"{authors}. {title}. {journal}. {year}"
                authors = parts[0].split(', et al')[0].split(', ')
                authors = [f"{a.split()[-1][0]}. {' '.join(a.split()[:-1])}" for a in authors]
                authors = ' and '.join(authors)
                title = f'"{parts[1].strip()}"'
                conference = ' '.join(parts[2:-1]).strip()
                year = parts[-1].strip()
                return f"{authors}. {title}. {conference}. {year}"
            if 'et al.' in parts[0]:
                authors = parts[0].split('et al.')[0].split(',')[0].split()
                authors = [f"{a[0]}. {' '.join(authors[1:])}" for a in [authors]]
            else:
                authors = parts[0].split(',')
                authors = [f"{a.split()[-1][0]}. {' '.join(a.split()[:-1])}" for a in authors]
            authors = ' and '.join(authors)
            title = f'"{parts[1]}"'
            if 'arXiv' in citation:
                conference = 'arXiv preprint arXiv:' + parts[2].split('arXiv:')[1].split(',')[0]
                year = parts[2].split(', ')[-1].strip('.')
                return f"{authors}. {title}. {conference} ({year})"
            else:
                conference = parts[2].split('(')[0].strip()
                year = parts[2].split('(')[1].split(')')[0]
                pages = parts[2].split('pp. ')[1].split('.')[0] if 'pp.' in citation else ''
                if pages:
                    return f"{authors}. {title}. In: {conference}, pp. {pages} ({year})"
                else:
                    return f"{authors}. {title}. In: {conference} ({year})"
    except (IndexError, ValueError):
        return f"Error: Unable to parse citation: {citation}"

with open('refer.txt', 'r') as file:
    citations = file.readlines()

lncs_citations = []
for citation in citations:
    preprocessed_citation = preprocess_citation(citation.strip())
    lncs_citation = convert_to_lncs(preprocessed_citation)
    lncs_citations.append(lncs_citation)

with open('lncs_references.txt', 'w') as file:
    file.write('\n'.join(lncs_citations))

print(f"LNCS格式引用已保存在 'lncs_references.txt' 文件中。")