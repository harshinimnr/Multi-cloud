# Multi-Cloud-Based Transportation Recommendation System

## Project Goal
Develop a multi-cloud-based transportation recommendation system that helps users find the nearest and best modes of transportation between two cities. This system integrates resources from multiple cloud providers such as GCP, Azure, and AWS to ensure interoperability, reliability, scalability, and redundancy.

## Objectives
1. Design and implement a transportation recommendation system.
2. Integrate resources from multiple cloud providers for redundancy and scalability.
3. Provide users with real-time transportation options based on their preferences.
4. Optimize route recommendations for time and environmental impact.
5. Evaluate the system's performance, scalability, and user satisfaction.

## Related Work
1. **Multi-Cloud Technology: Challenges and Solutions**
   - Foundational knowledge on transitioning between different cloud services and addressing parameters like time, cost, performance, and security.
2. **Managing Resources in Multi-Cloud Environments**
   - Insights into managing resources in multi-cloud environments and addressing interoperability challenges.
3. **Semantic-Interoperability in Multi-Cloud Platform Management**
   - Enhancing the system's interoperability and data exchange capabilities using semantic technologies.
4. **Cloud Technology in Transportation Systems**
   - Integration of cloud computing into transportation networks for smarter and more efficient systems.
5. **Data Protection, Privacy, and Open Research Challenges in Cloud Computing**
   - Addressing data protection and privacy challenges within cloud computing.

## Gap Analysis
1. **Lack of Unified Recommendation Systems**
   - Limited research on creating a unified recommendation system that leverages the strengths of multiple cloud providers for increased performance, reliability, and reduced costs.
2. **Limited Support for User Preferences**
   - Existing systems often focus on optimizing travel time and cost but lack support for environmental impact, accessibility, and other user preferences.

## Proposed Tasks
- Design a user interface (Web or Mobile App) for inputting origin and destination details and preferences.
- Develop algorithms to optimize transportation recommendations based on user preferences.
- Integrate resources from multiple cloud providers for efficient resource utilization.
- Store and synchronize transportation data and user preferences.
- Create a unified API layer to abstract the variations in APIs offered by different cloud providers.
- Conduct extensive testing for seamless data flow between cloud providers.

## Microservice Architecture
- **User Interface Service**: Enables user input and interaction.
- **Location Service**: Fetches user coordinates using the IPStack API.
- **Load Balance Service**: Optimizes resource utilization based on cloud provider metrics.
- **Routing Service**: Retrieves real-time transportation options from cloud providers.
- **Inter-Microservices Communication**: Uses HTTP requests for communication.
- **Scalability and Redundancy**: Achieved through modular microservices.

## Challenges and Solutions
- **Inter-Service Communication and Data Consistency**: Implementing RESTful APIs and strategies like eventual consistency to handle data synchronization challenges.

## Progress on Microservices Implementation
- **Location Service Integration**: Utilizes the IPStack API for accurate user coordinates.
- **Load Balance Service Enhancement**: Considers CPU utilization metrics for intelligent load distribution.
- **Routing Service Development**: Establishes connections with cloud providers for real-time data retrieval.
- **Testing and Optimization**: Extensive testing to validate reliability and performance.

## Conclusion
The adoption of a microservices architecture enhances scalability, maintainability, and flexibility, positioning the system for future enhancements and integrations.

## Key Considerations and Model Evaluation
- **Cloud Flexibility**: Adaptable configurations for seamless expansion to other cloud providers.
- **Multi-Cloud Strategy**: Mitigates vendor lock-in and enhances system resilience.
- **Supply Chain Focus**: Addresses the specific needs of supply chain logistics.

## Future Roadmap
- Hosting different services in diverse cloud environments to avoid reliance on a single cloud provider and ensure continuous operation of critical services.

## Project Links
- **Amazon Web Services**: [AWS URL](http://3.144.72.249)
- **Google Cloud Platform**: [GCP URL](https://tribal-bay-407302.oa.r.appspot.com)
- **Git**: [Repository](https://github.com/harshinimnr/Multi-cloud)

## References
1. Hamza Ali Imran, et al. "Multi-Cloud: A Comprehensive Review." IEEE. [Link](https://ieeexplore.ieee.org/abstract/document/9318176)
2. Victor Ion Munteanu, et al. "Multi-Cloud Resource Management: Cloud Service Interfacing." Journal of Cloud Computing. [Link](https://link.springer.com/article/10.1186/2192-113X-3-3)
3. Eleni Kamateri, et al. "Cloud4SOA: A Semantic-Interoperability PaaS Solution for Multi-cloud Platform Management and Portability." [Link](https://link.springer.com/chapter/10.1007/978-3-642-40651-5_6)
4. "Cloud Based Intelligent Transport System." [Link](https://www.sciencedirect.com/science/article/pii/S1877050915005621)
5. Junaid Hassan, et al. "The Rise of Cloud Computing: Data Protection, Privacy, and Open Research Challenges." [Link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9197654/)
