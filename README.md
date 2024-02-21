# DE-M7
DE project on Online Adverstising Platform
With increasing digitisation, there has been a tremendous boom in the field of online advertising as more and more companies are willing to pay large amounts of money in order to reach the customers via online platform. So, in this project, we will be building an online advertising platform.

The platform will have an interface for campaign managers to run the Ad campaign and another interface for the client to present the Ads and send the user action back to the advertising platform.
Through the campaign manager, the Ad instructions (New Ad Campaign, Stopping the existing Ad campaign) will be published to a Kafka Queue. The ‘Ad Manager’ will read the message from that Kafka queue and update the MySQL store accordingly.
An Ad Server will hold the auction of Ads for displaying the Ad to a user device. The auction winner will pay the amount bid by the second Ad. A user simulator will hit the Ad Server API for displaying Ads and send the user interaction feedback back to the feedback handler through API.
Upon receiving the user interaction feedback, the feedback handler will publish that event to another Kafka queue.
The User feedback handler will collect the feedback through the feedback API and it will be responsible for updating the leftover budget for the Ad campaign into MySQL. It will also publish the feedback to the internal Kafka queue, which will be later published to HIVE through user feedback writer for billing and archiving.
The whole system needs to be run for an hour and after that, the report generator will generate the bill report for all Ads displayed so far.

Databases:
Amazon Advertisements (https://www.kaggle.com/datasets/sachsene/amazons-advertisements): This data set contains data pertaining to the advertisement from Amazon (stand by the end of 2019)

ADS 16 data set (https://www.kaggle.com/datasets/groffo/ads16-dataset): This data set was used to ascertain the user preference for the advertisement data. 

Advertising (https://www.kaggle.com/datasets/tbyrnes/advertising): This data set contains the demographics and the internet usage patterns of the users.

![Approach](https://github.com/AbhilashaGarg03/DE-M7/assets/107549962/7a0c9c81-fdb3-4ea9-9a2b-d39fa414ebeb)
