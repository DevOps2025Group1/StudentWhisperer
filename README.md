# Dialogue-Based Student Portal Design using a Large Language Model (LLM)

## Contact  
**Nafis Tanveer Islam**  
📧 [n.t.islam@uva.nl](mailto:n.t.islam@uva.nl)  

## Description  
A school wants to implement a **dialogue-based “Student Management Portal”**, allowing students to **chat** with a system regarding their **course results, graduation requirements,** and **areas for improvement** using **microservices**.  

The portal should:  
- Allow students to ask about **their** results.  
- Help them identify **areas for improvement**.  
- Show the **number of remaining courses** required for graduation.  
- Ensure the system **does not get overwhelmed** due to excessive queries, leading to **high costs**.  

---

## Requirements  

### **Core Functionalities:**  
1. Develop a **secure student portal** allowing students to log in.  
2. Maintain individual student records in **any chosen format** (Relational DB, Non-Relational DB, CSV, JSON, etc.).  
3. Ensure **students cannot access** another student’s performance data.  
4. Provide a **User Interface (UI)** for profile **viewing and editing**.  
5. Implement a **Chat interface** where students can:  
   - Ask about their **performance**.  
   - Check their **scores** in different subjects.  
   - View **remaining courses** required for graduation.  
   - (⚠️ Ensure cost estimation and monitoring of LLM usage).  

---

## **Expected Output**  

### **Minimum Requirements:**  
✅ A working **cloud application** with:  
- A **secure, scalable, and user-friendly** student portal.  
- **Integration of a dialogue system** using LLM (e.g., OpenAI, Hugging Face).  
- **Login & profile management** with **information exclusivity** for students.  
- A **Monitoring System** to track usage and restrict excessive queries.  

### **Advanced Deliverables (If Time Allows):**  
1. **Identify and analyze performance bottlenecks**:  
   - Does the system slow down with multiple concurrent users?  
   - Explain where and why the delay occurs.  

2. **Optimize and speed up the dialogue system**.  

3. **Implement a cost-control protocol** to limit excessive traffic.  

---

## **References**  
1. [Student Result Management System](https://github.com/shubhamsatishkumbhar/Student-Result-ManagementSystem-SRMS-)  
2. [Falcon-LLM Education Platform](https://github.com/roshnn24/Falcon-LLM-Education-Platform)  
