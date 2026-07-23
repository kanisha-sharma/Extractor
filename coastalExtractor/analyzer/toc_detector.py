import fitz


class TOCDetector:

    def __init__(self, document: fitz.Document):

        self.document = document

    def detect(self):

        toc = self.document.get_toc(simple=False)

        if toc:

            return self.__parse_builtin_toc(toc)

        return self.__search_for_toc_pages()

    def __parse_builtin_toc(self, toc):

        headings = []

        for item in toc:

            level = item[0]

            title = item[1].strip()

            page = item[2]

            headings.append(

                {
                    "title": title,
                    "page": page,
                    "level": level
                }

            )

        return headings

    def __search_for_toc_pages(self):

        toc_entries = []

        max_pages = min(15, len(self.document))

        for page_number in range(max_pages):

            page = self.document[page_number]

            text = page.get_text()

            lower = text.lower()

            if "table of contents" in lower or "contents" in lower:

                toc_entries.extend(

                    self.__extract_entries(text)

                )

        return toc_entries

    def __extract_entries(self, text):

        entries = []

        lines = text.split("\n")

        for line in lines:

            line = line.strip()

            if len(line) < 3:
                continue

            tokens = line.split()

            if len(tokens) < 2:
                continue

            if tokens[-1].isdigit():

                page = int(tokens[-1])

                title = " ".join(tokens[:-1])

                entries.append(

                    {

                        "title": title,

                        "page": page,

                        "level": 1

                    }

                )

        return entries