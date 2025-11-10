// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificateVerification {
    struct Certificate {
        string certificateId;
        string hash;
        string studentName;
        string courseName;
        string issueDate;
        uint256 timestamp;
        bool exists;
    }
    
    mapping(string => Certificate) public certificates;
    string[] public certificateHashes;
    
    event CertificateIssued(
        string indexed certificateId,
        string indexed hash,
        string studentName
    );
    
    function issueCertificate(
        string memory _certificateId,
        string memory _hash,
        string memory _studentName,
        string memory _courseName,
        string memory _issueDate
    ) public {
        require(!certificates[_hash].exists, "Certificate with this hash already exists");
        
        certificates[_hash] = Certificate({
            certificateId: _certificateId,
            hash: _hash,
            studentName: _studentName,
            courseName: _courseName,
            issueDate: _issueDate,
            timestamp: block.timestamp,
            exists: true
        });
        
        certificateHashes.push(_hash);
        
        emit CertificateIssued(_certificateId, _hash, _studentName);
    }
    
    function verifyCertificate(string memory _hash) public view returns (bool) {
        return certificates[_hash].exists;
    }
    
    function getCertificate(string memory _hash) public view returns (
        string memory certificateId,
        string memory studentName,
        string memory courseName,
        string memory issueDate,
        uint256 timestamp
    ) {
        require(certificates[_hash].exists, "Certificate not found");
        
        Certificate memory cert = certificates[_hash];
        return (
            cert.certificateId,
            cert.studentName,
            cert.courseName,
            cert.issueDate,
            cert.timestamp
        );
    }
    
    function getTotalCertificates() public view returns (uint256) {
        return certificateHashes.length;
    }
}

