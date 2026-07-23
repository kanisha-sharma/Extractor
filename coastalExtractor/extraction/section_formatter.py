from __future__ import annotations



class SectionFormatter:
    """
    Formats extracted sections
    for API/frontend output.
    """



    def format_json(
        self,
        response
    ):

        return {

            "section":

                {

                    "id":
                        response.section_id,


                    "title":
                        response.title,


                    "pages":
                        {

                            "start":
                                response.page_start,

                            "end":
                                response.page_end

                        }

                },


            "content":

                response.content,


            "metadata":

                response.metadata

        }



    def format_summary(
        self,
        response
    ):


        return {


            "title":

                response.title,


            "pages":

                f"{response.page_start}-{response.page_end}",


            "tables":

                response.metadata.get(
                    "tables",
                    0
                ),


            "paragraphs":

                response.metadata.get(
                    "paragraphs",
                    0
                )


        }