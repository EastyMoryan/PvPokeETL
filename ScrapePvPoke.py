import csv


# Ranking is 1500 for GL, 2500 for UL, 10000 for ML
def scrape_format(ranking, resultsdict, formsdict):
    filename = "RankingsExports/cp{}_all_overall_rankings.csv".format(ranking)
    if ranking == 1500:
        league = "GL"
    elif ranking == 2500:
        league = "UL"
    else:
        league = "ML"

    with open(filename, newline="\n") as csvfile:
        myreader = csv.DictReader(csvfile)
        for i, row in enumerate(myreader):
            parsed_row = row["Pokemon"].split()
            form = None
            shadow = False
            for token in parsed_row:
                if token[0] != "(":
                    continue
                if token == "(Shadow)":
                    shadow = True
                    continue
                form = token[1:]
                if form[-1] == ")":
                    form = form[:-1]
            dexnum = int(row["Dex"])
            if not form:
                if dexnum not in resultsdict:
                    resultsdict[dexnum] = {"dexnum": dexnum}
                shadow_aware_league = "{}{}".format(league, "(S)" if shadow else "")
                if shadow_aware_league not in resultsdict[dexnum]:
                    resultsdict[dexnum][shadow_aware_league] = i+1
            else:
                if i > 130 or (league == "ML" and i > 50):
                    continue
                if (dexnum, form) not in formsdict:
                    formsdict[(dexnum, form)] = {"dexnum": dexnum, "form": form}
                shadow_aware_league = "{}{}".format(league, "(S)" if shadow else "")
                if shadow_aware_league not in formsdict[(dexnum, form)]:
                    formsdict[(dexnum, form)][shadow_aware_league] = i + 1
    return resultsdict, formsdict


def dump_to_csv(results):
    leagues = ["GL", "UL", "ML"]
    fields = ["dexnum"] + leagues + [league+"(S)" for league in leagues]
    filename = "PvPokeScrape.csv"

    with open(filename, 'w', newline="") as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields, restval="IGNORE", extrasaction="raise")

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        for i in range(1, 1025):
            if i in results:
                writer.writerow(results[i])
            else:
                writer.writerow({"dexnum": i})


def dump_to_csv_with_form(formsdict):
    leagues = ["GL", "UL", "ML"]
    fields = ["dexnum"] + ["form"] + leagues + [league+"(S)" for league in leagues]
    filename = "PvPokeScrapeForms.csv"

    with open(filename, 'w', newline="") as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields, restval="IGNORE", extrasaction="raise")

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        for key in formsdict:
            writer.writerow(formsdict[key])


def scrape_all():
    results = dict()
    forms = dict()
    # scrape GL, put into list
    results, forms = scrape_format(1500, results, forms)
    # scrape UL, put into list
    results, forms = scrape_format(2500, results, forms)
    # scrape ML, put into list
    results, forms = scrape_format(10000, results, forms)
    # dump to CSV
    dump_to_csv(results)
    dump_to_csv_with_form(forms)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrape_all()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
