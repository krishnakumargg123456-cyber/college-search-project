def recommend_colleges(percentage, jee, budget):

    colleges = [

        {
            "name": "PSIT Kanpur",
            "min_percentage": 60,
            "min_jee": 20,
            "fees": 150000
        },

        {
            "name": "KIET Ghaziabad",
            "min_percentage": 70,
            "min_jee": 40,
            "fees": 180000
        },

        {
            "name": "ABES Engineering College",
            "min_percentage": 65,
            "min_jee": 30,
            "fees": 170000
        },

        {
            "name": "GL Bajaj",
            "min_percentage": 75,
            "min_jee": 50,
            "fees": 190000
        }

    ]

    recommended = []

    for college in colleges:

        if (
            percentage >= college["min_percentage"]
            and jee >= college["min_jee"]
            and budget >= college["fees"]
        ):
            recommended.append(college)

    return recommended