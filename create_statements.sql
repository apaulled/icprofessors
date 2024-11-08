create table offices(
    id int auto_increment,
    location varchar(64),
    primary key(id)
);

create table departments(
    id int auto_increment,
    name varchar(64),
    primary key(id)
);

create table department_sections(
    id int auto_increment,
    title varchar(64),
    primary key(id)
);

create table specialties(
    id int auto_increment,
    name varchar(256),
    primary key(id)
);

create table jobs(
    id int auto_increment,
    name varchar(256),
    primary key(id)
);

create table schools(
    id int auto_increment,
    name varchar(64),
    primary key(id)
);

create table faculty(
    id binary(12),
    name varchar(30),
    school_id int,
    department_id int,
    department_section_id int,
    job_id int,
    office_id int,
    phone char(10),
    email varchar(32),
    url varchar(64),
    primary key(id),
    foreign key (school_id) references schools(id),
    foreign key (department_id) references departments(id),
    foreign key (department_section_id) references department_sections(id),
    foreign key (job_id) references jobs(id),
    foreign key (office_id) references offices(id)
);

create table faculty_specialties(
    faculty_id binary(12),
    specialty_id int,
    foreign key (faculty_id) references faculty(id),
    foreign key (specialty_id) references specialties(id)
);