package com.example.project1.repository;

import com.example.project1.model.CorporateEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface CorporateRepository extends JpaRepository<CorporateEntity, Long> {
    Optional<CorporateEntity> findByCompanyCode(String companyCode);
}
