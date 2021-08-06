import datetime as dt
import pandas as pd

#mediafacts=pd.read_csv(r"Campaigns\campaigns_unified.csv")
#mediaplan=pd.read_csv(r"Mediaplan\mp_processed\Adverity-export_Plan.csv")



###########################################
def mp_match(mediaplan, mediafacts):
    df_facts = mediafacts[["Campaign Name", "Datasource"]]
    df_facts['is_fact'] = True
    df_mediaplan = mediaplan[["Campaign Name", "Mediaplan", "Campaign Mp Label", "Datasource"]]
    df_mediaplan['is_campaign'] = True

    df_join = pd.merge(df_facts, df_mediaplan, on='Campaign Name', how='outer')

    matching_campaigns = df_join[(df_join['is_fact'] == True) & (df_join['is_campaign'] == True)]
    unmatching_campaigns = df_join[(df_join['is_fact'] != True) & (df_join['is_campaign'] == True)]
    print("matched:",matching_campaigns, matching_campaigns.columns)
    print("unmatched",unmatching_campaigns, unmatching_campaigns.columns)

    matching_campaigns[["Campaign Name", "Mediaplan", "Campaign Mp Label", "Datasource_y"]].to_csv("matching_campaigns.csv", index=False)
    unmatching_campaigns[["Campaign Name", "Mediaplan","Campaign Mp Label", "Datasource_y"]].to_csv("unmatching_campaigns.csv", index=False)

    lmatching_campaigns = len(matching_campaigns)
    lunmatching_campaigns = len(unmatching_campaigns)
    m_rate = (lmatching_campaigns/(lmatching_campaigns + lunmatching_campaigns))*100
    print("Matching: ", lmatching_campaigns)
    print("Unmatching: ", lunmatching_campaigns)
    print("match rate:", m_rate, "%")

    return 0
